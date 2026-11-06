"""
Email notification helper for GeoAlert AI.

Provides a send_email() function that sends alert notifications via SMTP.
SMTP configuration is read from environment variables or Streamlit secrets
(never hardcoded). Recipient addresses are supplied explicitly by the caller
(never guessed or defaulted).
"""

import os
import smtplib
import ssl
from email.message import EmailMessage
from typing import List, Tuple

# SMTP configuration keys (read from environment or Streamlit secrets)
SMTP_HOST_KEY = "SMTP_HOST"
SMTP_PORT_KEY = "SMTP_PORT"
SMTP_USER_KEY = "SMTP_USER"
SMTP_PASSWORD_KEY = "SMTP_PASSWORD"
SMTP_USE_TLS_KEY = "SMTP_USE_TLS"
SMTP_FROM_EMAIL_KEY = "SMTP_FROM_EMAIL"

DEFAULT_SMTP_PORT = 587
DEFAULT_SMTP_TIMEOUT = 10  # seconds


def _get_config(key: str, default=None):
    """Read a config value from Streamlit secrets first, then environment.

    Streamlit secrets take precedence when running under Streamlit;
    environment variables are used as a fallback.
    """
    try:
        import streamlit as st

        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Streamlit not available or secrets not configured; fall through
        pass
    return os.environ.get(key, default)


def parse_recipients(recipients_input: str) -> List[str]:
    """Parse a comma-separated recipient string into a list of addresses.

    Strips whitespace around each address and drops empty entries.
    Returns an empty list if the input is None or blank.
    """
    if not recipients_input or not recipients_input.strip():
        return []
    return [addr.strip() for addr in recipients_input.split(",") if addr.strip()]


def _is_smtp_configured() -> bool:
    """Return True if the minimum SMTP configuration is present."""
    host = _get_config(SMTP_HOST_KEY)
    user = _get_config(SMTP_USER_KEY)
    password = _get_config(SMTP_PASSWORD_KEY)
    from_email = _get_config(SMTP_FROM_EMAIL_KEY)
    return bool(host and user and password and from_email)


def send_email(subject: str, message: str, to_emails: str) -> Tuple[bool, str]:
    """Send an email alert notification via SMTP.

    Parameters
    ----------
    subject : str
        Email subject line.
    message : str
        Plain-text email body.
    to_emails : str
        Comma-separated recipient email addresses supplied explicitly
        by the caller. An empty or blank string is treated as "no
        recipients" and returns (False, error message).

    Returns
    -------
    (success, message) : tuple of (bool, str)
        success is True only when the SMTP server accepted the message.
        message is a human-readable status or error description.

    Raises
    ------
    ValueError
        If recipient input is empty or all addresses are malformed.
    """
    recipients = parse_recipients(to_emails)
    if not recipients:
        return False, "No recipient email addresses provided."

    from_email = _get_config(SMTP_FROM_EMAIL_KEY)
    if not from_email:
        return False, "SMTP_FROM_EMAIL is not configured."

    if not _is_smtp_configured():
        missing = []
        if not _get_config(SMTP_HOST_KEY):
            missing.append("SMTP_HOST")
        if not _get_config(SMTP_USER_KEY):
            missing.append("SMTP_USER")
        if not _get_config(SMTP_PASSWORD_KEY):
            missing.append("SMTP_PASSWORD")
        return False, (
            "SMTP is not fully configured. Missing: "
            + ", ".join(missing)
            + ". Set these as environment variables or Streamlit secrets."
        )

    host = _get_config(SMTP_HOST_KEY)
    port = int(_get_config(SMTP_PORT_KEY, DEFAULT_SMTP_PORT) or DEFAULT_SMTP_PORT)
    user = _get_config(SMTP_USER_KEY)
    password = _get_config(SMTP_PASSWORD_KEY)
    use_tls = str(_get_config(SMTP_USE_TLS_KEY, "true")).lower() != "false"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = ", ".join(recipients)
    msg.set_content(message)

    context = ssl.create_default_context()

    try:
        if use_tls and port == 465:
            # SMTPS over implicit TLS
            with smtplib.SMTP_SSL(host, port, timeout=DEFAULT_SMTP_TIMEOUT, context=context) as server:
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=DEFAULT_SMTP_TIMEOUT) as server:
                server.ehlo()
                if use_tls:
                    server.starttls(context=context)
                    server.ehlo()
                server.login(user, password)
                server.send_message(msg)
    except smtplib.SMTPAuthenticationError as exc:
        return False, "SMTP authentication failed. Check SMTP_USER and SMTP_PASSWORD."
    except smtplib.SMTPConnectError as exc:
        return False, f"Could not connect to SMTP server at {host}:{port}."
    except smtplib.SMTPException as exc:
        return False, f"SMTP error while sending email: {exc}"
    except OSError as exc:
        return False, f"Network error contacting SMTP server: {exc}"
    except Exception as exc:
        # Never expose internal exception details (could contain credentials)
        return False, "An unexpected error occurred while sending the email."

    return True, f"Alert email sent successfully to {len(recipients)} recipient(s)."