"""
Phase 3A regression tests: Email notification fix.

Tests for notifications.py send_email():
- Valid recipient addresses (mocked SMTP)
- Empty and malformed recipient input
- Missing SMTP configuration
- Successful mocked delivery
- SMTP connection and authentication failures
- No credentials appear in user-facing error messages
- send_email() is defined and callable

These tests never contact a real SMTP server.
"""

import sys
import os
from unittest.mock import MagicMock, patch

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import notifications  # noqa: E402


@pytest.fixture
def clean_env(monkeypatch):
    """Remove SMTP env vars so tests start from an unconfigured state."""
    for key in [
        "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
        "SMTP_USE_TLS", "SMTP_FROM_EMAIL",
    ]:
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def smtp_configured(monkeypatch):
    """Set minimal SMTP configuration via environment variables."""
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "user@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "secret123")
    monkeypatch.setenv("SMTP_USE_TLS", "true")
    monkeypatch.setenv("SMTP_FROM_EMAIL", "alerts@example.com")


class TestParseRecipients:
    def test_valid_single_recipient(self):
        assert notifications.parse_recipients("alice@example.com") == ["alice@example.com"]

    def test_valid_multiple_recipients(self):
        result = notifications.parse_recipients("alice@example.com, bob@example.com")
        assert result == ["alice@example.com", "bob@example.com"]

    def test_recipients_with_whitespace(self):
        result = notifications.parse_recipients("  alice@example.com ,  bob@example.com  ")
        assert result == ["alice@example.com", "bob@example.com"]

    def test_empty_string(self):
        assert notifications.parse_recipients("") == []

    def test_blank_string(self):
        assert notifications.parse_recipients("   ") == []

    def test_none_input(self):
        assert notifications.parse_recipients(None) == []

    def test_trailing_comma_dropped(self):
        result = notifications.parse_recipients("alice@example.com,")
        assert result == ["alice@example.com"]


class TestSmtpConfigured:
    def test_not_configured_when_empty(self, clean_env):
        assert notifications._is_smtp_configured() is False

    def test_configured_when_all_present(self, smtp_configured):
        assert notifications._is_smtp_configured() is True

    def test_missing_host(self, monkeypatch):
        monkeypatch.setenv("SMTP_USER", "u")
        monkeypatch.setenv("SMTP_PASSWORD", "p")
        monkeypatch.setenv("SMTP_FROM_EMAIL", "f@example.com")
        assert notifications._is_smtp_configured() is False


class TestSendEmail:
    def test_empty_recipients_returns_failure(self, smtp_configured):
        success, msg = notifications.send_email("Subject", "Body", "")
        assert success is False
        assert "No recipient email addresses" in msg

    def test_blank_recipients_returns_failure(self, smtp_configured):
        success, msg = notifications.send_email("Subject", "Body", "   ")
        assert success is False
        assert "No recipient email addresses" in msg

    def test_missing_smtp_config_returns_failure(self, clean_env):
        success, msg = notifications.send_email(
            "Subject", "Body", "alice@example.com"
        )
        assert success is False
        assert "not configured" in msg

    def test_missing_full_smtp_config_returns_failure(self, monkeypatch):
        # Set FROM_EMAIL but leave host/user/password missing
        monkeypatch.setenv("SMTP_FROM_EMAIL", "alerts@example.com")
        success, msg = notifications.send_email(
            "Subject", "Body", "alice@example.com"
        )
        assert success is False
        assert "SMTP is not fully configured" in msg

    def test_missing_smtp_config_does_not_leak_credentials(self, monkeypatch):
        monkeypatch.setenv("SMTP_PASSWORD", "very_secret_password")
        success, msg = notifications.send_email(
            "Subject", "Body", "alice@example.com"
        )
        assert success is False
        assert "very_secret_password" not in msg
        assert "secret" not in msg.lower()

    @patch("notifications.smtplib.SMTP")
    def test_successful_delivery(self, mock_smtp_class, smtp_configured):
        mock_server = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_server

        success, msg = notifications.send_email(
            "Rockfall Alert", "Warning body", "alice@example.com, bob@example.com"
        )

        assert success is True
        assert "sent successfully" in msg
        assert "2 recipient(s)" in msg
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

    @patch("notifications.smtplib.SMTP")
    def test_smtp_auth_failure(self, mock_smtp_class, smtp_configured):
        import smtplib
        mock_server = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_server
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "bad creds")

        success, msg = notifications.send_email("Subject", "Body", "alice@example.com")

        assert success is False
        assert "authentication failed" in msg.lower()
        assert "secret123" not in msg
        assert "user@example.com" not in msg

    @patch("notifications.smtplib.SMTP")
    def test_smtp_connect_failure(self, mock_smtp_class, smtp_configured):
        import smtplib
        mock_smtp_class.side_effect = smtplib.SMTPConnectError(421, "service not available")

        success, msg = notifications.send_email("Subject", "Body", "alice@example.com")

        assert success is False
        assert "Could not connect" in msg
        assert "smtp.example.com" in msg

    @patch("notifications.smtplib.SMTP")
    def test_smtp_generic_error(self, mock_smtp_class, smtp_configured):
        mock_server = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_server
        mock_server.login.side_effect = Exception("something unexpected")

        success, msg = notifications.send_email("Subject", "Body", "alice@example.com")

        assert success is False
        assert "unexpected error" in msg.lower()
        assert "something unexpected" not in msg

    def test_send_email_is_callable(self):
        assert callable(notifications.send_email)