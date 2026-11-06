"""
Phase 4A regression tests: Help desk attachment security.

Tests for secure_attachment_filename() and save_helpdesk_attachment():
- Normal valid attachment
- Filename containing ../
- Filename containing Windows-style ..\
- Absolute or drive-qualified paths
- Attempts to escape the attachment directory
- Two attachments with the same original filename (no overwrite)
- Empty attachments and oversized files
- Unsupported file types
- Write failures

These tests never write to real user data or bundled datasets.
They use temporary directories via monkeypatch.
"""

import sys
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import model  # noqa: E402


@pytest.fixture
def tmp_attach_dir(monkeypatch):
    """Redirect HELPDESK_ATTACHMENT_DIR to a temporary directory."""
    tmp = tempfile.mkdtemp(prefix="geoalert_attach_")
    monkeypatch.setattr(model, "HELPDESK_ATTACHMENT_DIR", tmp)
    return tmp


class TestSecureAttachmentFilename:
    def test_valid_filename(self):
        safe, err = model.secure_attachment_filename("report.pdf")
        assert err is None
        assert safe == "report.pdf"

    def test_valid_filename_with_multiple_dots(self):
        safe, err = model.secure_attachment_filename("seismic.log.2026.csv")
        assert err is None
        assert safe == "seismic.log.2026.csv"

    def test_path_traversal_dotdot_slash(self):
        safe, err = model.secure_attachment_filename("../../../etc/passwd")
        assert safe is None
        assert err is not None
        assert "invalid path" in err.lower()

    def test_path_traversal_dotdot_backslash(self):
        safe, err = model.secure_attachment_filename("..\\..\\windows\\win.ini")
        assert safe is None
        assert err is not None
        assert "invalid path" in err.lower()

    def test_absolute_path(self):
        safe, err = model.secure_attachment_filename("/etc/passwd")
        assert safe is None
        assert err is not None

    def test_drive_qualified_path(self):
        safe, err = model.secure_attachment_filename("C:\\Windows\\System32\\config\\sam")
        assert safe is None
        assert err is not None

    def test_empty_filename(self):
        safe, err = model.secure_attachment_filename("")
        assert safe is None
        assert err is not None

    def test_none_filename(self):
        safe, err = model.secure_attachment_filename(None)
        assert safe is None
        assert err is not None

    def test_unsupported_extension(self):
        safe, err = model.secure_attachment_filename("malware.exe")
        assert safe is None
        assert err is not None
        assert "not allowed" in err.lower()

    def test_allowed_extensions(self):
        for ext in [".png", ".jpg", ".jpeg", ".csv", ".pdf"]:
            safe, err = model.secure_attachment_filename(f"file{ext}")
            assert err is None, f"Extension {ext} should be allowed: {err}"
            assert safe == f"file{ext}"


class TestSaveHelpdeskAttachment:
    def test_valid_attachment_saved(self, tmp_attach_dir):
        server_path, display_name, err = model.save_helpdesk_attachment(
            b"valid pdf content", "report.pdf"
        )
        assert err is None
        assert server_path is not None
        assert display_name == "report.pdf"
        assert os.path.exists(server_path)
        abs_server = os.path.abspath(server_path)
        abs_dir = os.path.abspath(tmp_attach_dir)
        assert abs_server == abs_dir or abs_server.startswith(abs_dir + os.sep)
        with open(server_path, "rb") as f:
            assert f.read() == b"valid pdf content"

    def test_attachment_uses_uuid_not_original_name(self, tmp_attach_dir):
        server_path, _, _ = model.save_helpdesk_attachment(b"data", "report.pdf")
        filename = os.path.basename(server_path)
        assert "report" not in filename
        assert filename.endswith(".pdf")

    def test_path_traversal_filename_blocked(self, tmp_attach_dir):
        server_path, _, err = model.save_helpdesk_attachment(
            b"data", "../../../etc/passwd"
        )
        assert server_path is None
        assert err is not None

    def test_dotdot_backslash_filename_blocked(self, tmp_attach_dir):
        server_path, _, err = model.save_helpdesk_attachment(
            b"data", "..\\..\\windows\\win.ini"
        )
        assert server_path is None
        assert err is not None

    def test_absolute_path_filename_blocked(self, tmp_attach_dir):
        server_path, _, err = model.save_helpdesk_attachment(
            b"data", "/etc/passwd"
        )
        assert server_path is None
        assert err is not None

    def test_unsupported_extension_blocked(self, tmp_attach_dir):
        server_path, _, err = model.save_helpdesk_attachment(
            b"data", "malware.exe"
        )
        assert server_path is None
        assert err is not None

    def test_empty_file_rejected(self, tmp_attach_dir):
        server_path, _, err = model.save_helpdesk_attachment(b"", "empty.pdf")
        assert server_path is None
        assert err is not None
        assert "empty" in err.lower()

    def test_oversized_file_rejected(self, tmp_attach_dir, monkeypatch):
        monkeypatch.setattr(model, "MAX_ATTACHMENT_SIZE_BYTES", 10)
        server_path, _, err = model.save_helpdesk_attachment(
            b"this is more than 10 bytes", "small.pdf"
        )
        assert server_path is None
        assert err is not None

    def test_same_original_filename_no_overwrite(self, tmp_attach_dir):
        p1, _, e1 = model.save_helpdesk_attachment(b"first", "same.pdf")
        p2, _, e2 = model.save_helpdesk_attachment(b"second", "same.pdf")
        assert e1 is None
        assert e2 is None
        assert p1 is not None
        assert p2 is not None
        assert p1 != p2
        assert os.path.exists(p1)
        assert os.path.exists(p2)
        with open(p1, "rb") as f:
            assert f.read() == b"first"
        with open(p2, "rb") as f:
            assert f.read() == b"second"

    def test_attachment_stays_inside_directory(self, tmp_attach_dir):
        server_path, _, err = model.save_helpdesk_attachment(b"data", "safe.pdf")
        assert err is None
        abs_server = os.path.abspath(server_path)
        abs_dir = os.path.abspath(tmp_attach_dir)
        assert abs_server == abs_dir or abs_server.startswith(abs_dir + os.sep)

    def test_write_failure_handled(self, tmp_attach_dir, monkeypatch):
        import builtins

        def failing_open(*args, **kwargs):
            raise OSError("simulated disk failure")

        monkeypatch.setattr(builtins, "open", failing_open)
        try:
            server_path, _, err = model.save_helpdesk_attachment(
                b"data", "fail.pdf"
            )
            assert server_path is None
            assert err is not None
        finally:
            monkeypatch.undo()


class TestTicketCompatibility:
    def test_ticket_data_contains_safe_fields(self):
        import inspect
        source = inspect.getsource(model)
        assert 'f"{ticket_id}_{uploaded_file.name}"' not in source
        assert 'with open(file_name' not in source
        assert "save_helpdesk_attachment" in source
        assert "Attachment_Display" in source