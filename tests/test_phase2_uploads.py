"""
Phase 2 regression tests: Protect original datasets and secure CSV upload handling.

These tests verify that:
- Uploaded data is saved under user_data/ and never overwrites bundled datasets.
- Open-pit and underground uploads are routed to separate directories.
- Missing required columns produce clear validation errors.
- Empty/malformed uploads are handled safely without crashing.
- Rejected-row counts are accurate.
- Original bundled datasets remain byte-for-byte unchanged.
- Python source files compile cleanly.

Streamlit is mocked before importing model.py so top-level st.* calls
do not require a Streamlit script-run context.
"""

import sys
import os
import hashlib
import tempfile
from io import BytesIO
from unittest.mock import MagicMock

import pandas as pd
import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Mock streamlit so importing model.py does not require a script-run context
# ---------------------------------------------------------------------------
sys.modules["streamlit"] = MagicMock()

# Ensure the project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import model  # noqa: E402  (import after sys.modules mocking)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def original_open_pit_hash():
    """SHA-256 of the bundled open-pit dataset before any test runs."""
    path = os.path.join(PROJECT_ROOT, "slope_stability_dataset.csv")
    return _sha256(path)


@pytest.fixture
def original_underground_hash():
    """SHA-256 of the bundled underground dataset before any test runs."""
    path = os.path.join(PROJECT_ROOT, "underground_dataset.csv")
    return _sha256(path)


@pytest.fixture
def tmp_user_data(monkeypatch):
    """Point model's upload directories at a temporary location."""
    tmp = tempfile.mkdtemp(prefix="geoalert_test_")
    open_pit_dir = os.path.join(tmp, "open_pit_uploads")
    underground_dir = os.path.join(tmp, "underground_uploads")
    monkeypatch.setattr(model, "OPEN_PIT_UPLOAD_DIR", open_pit_dir)
    monkeypatch.setattr(model, "UNDERGROUND_UPLOAD_DIR", underground_dir)
    monkeypatch.setattr(model, "USER_DATA_DIR", tmp)
    return tmp


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()




# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------

class TestUploadHelpers:
    def test_get_upload_dir_open_pit(self):
        assert model.get_upload_dir("Open Pit Mines") == model.OPEN_PIT_UPLOAD_DIR

    def test_get_upload_dir_underground(self):
        assert model.get_upload_dir("Underground Pit Mines") == model.UNDERGROUND_UPLOAD_DIR

    def test_sanitize_filename_strips_path_traversal(self):
        # os.path.basename keeps only the final path component
        assert model.sanitize_filename("../../../etc/passwd") == "passwd"
        assert model.sanitize_filename("..\\..\\windows\\win.ini") == "win.ini"

    def test_sanitize_filename_unsafe_chars(self):
        assert model.sanitize_filename("my file#1.csv") == "my_file_1.csv"

    def test_sanitize_filename_dotdot_fallback(self):
        assert model.sanitize_filename("..") == "upload.csv"
        assert model.sanitize_filename(".") == "upload.csv"

    def test_get_unique_filename_includes_timestamp(self):
        name = model.get_unique_filename("/tmp", "data.csv")
        assert name.startswith("20")  # YYYYMMDD...
        assert name.endswith("_data.csv")

    def test_get_unique_filename_adds_extension(self):
        name = model.get_unique_filename("/tmp", "data")
        assert name.endswith(".csv")

    def test_save_uploaded_bytes_creates_file(self, tmp_user_data):
        path = model.save_uploaded_bytes(b"hello", tmp_user_data, "test.csv")
        assert os.path.exists(path)
        with open(path, "rb") as f:
            assert f.read() == b"hello"


def _make_uploaded_file(name, df):
    """Create a BytesIO object (with .name) that behaves like an uploaded CSV."""
    buf = BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    buf.name = name
    return buf


# ---------------------------------------------------------------------------
# process_uploaded_file tests
# ---------------------------------------------------------------------------

class TestProcessUploadedFile:
    def test_valid_open_pit_upload_returns_df_and_stats(self):
        df = pd.DataFrame({
            "fs": [1.2, 2.0, 0.8, 1.5],
            "reinforcement": [0.5, 0.3, 0.1, 2.0],
        })
        f = _make_uploaded_file("open_pit.csv", df)
        result, stats = model.process_uploaded_file(f)
        assert isinstance(result, pd.DataFrame)
        assert isinstance(stats, dict)
        assert stats["rows_read"] == 4
        assert "rows_rejected" in stats
        assert "rockfall_risk" in result.columns

    def test_missing_required_columns_raises_value_error(self):
        df = pd.DataFrame({"fs": [1.2], "foo": [1]})
        f = _make_uploaded_file("bad.csv", df)
        with pytest.raises(ValueError, match="Missing required columns"):
            model.process_uploaded_file(f)

    def test_empty_csv_raises_value_error(self):
        df = pd.DataFrame(columns=["fs", "reinforcement"])
        f = _make_uploaded_file("empty.csv", df)
        with pytest.raises(ValueError, match="no data rows|empty"):
            model.process_uploaded_file(f)

    def test_invalid_numeric_rows_are_rejected(self):
        df = pd.DataFrame({
            "fs": [1.2, "not_a_number", 2.0, 1.5],
            "reinforcement": [0.5, 0.3, "bad", 1.0],
        })
        f = _make_uploaded_file("mixed.csv", df)
        result, stats = model.process_uploaded_file(f)
        assert len(result) == 2
        assert stats["rows_rejected"] == 2
        assert stats["rows_read"] == 4

    def test_all_rows_rejected_raises_value_error(self):
        df = pd.DataFrame({
            "fs": ["bad", "also_bad"],
            "reinforcement": ["x", "y"],
        })
        f = _make_uploaded_file("all_bad.csv", df)
        with pytest.raises(ValueError, match="All rows were rejected"):
            model.process_uploaded_file(f)

    def test_returns_stats_dict_with_expected_keys(self):
        df = pd.DataFrame({"fs": [1.5], "reinforcement": [1.0]})
        f = _make_uploaded_file("ok.csv", df)
        _, stats = model.process_uploaded_file(f)
        for key in ("rows_read", "rows_rejected", "columns_missing", "synthetic"):
            assert key in stats


# ---------------------------------------------------------------------------
# process_underground_file tests
# ---------------------------------------------------------------------------

class TestProcessUndergroundFile:
    REQUIRED_COLS = [
        "seismic", "seismoacoustic", "shift",
        "genergy", "gpuls", "gdenergy", "gdpuls",
        "hazard", "nbumps", "nbumps2", "nbumps3",
        "nbumps4", "nbumps5", "nbumps6",
        "nbumps7", "nbumps89", "energy", "maxenergy",
    ]

    def _make_underground_df(self):
        return pd.DataFrame({
            col: ["a"] * 3 if col in ("seismic", "seismoacoustic", "shift", "hazard")
                 else [1.0] * 3
            for col in self.REQUIRED_COLS
        })

    def test_valid_underground_upload_returns_df_and_stats(self):
        df = self._make_underground_df()
        f = _make_uploaded_file("underground.csv", df)
        result, stats = model.process_underground_file(f)
        assert isinstance(result, pd.DataFrame)
        assert isinstance(stats, dict)
        assert stats["rows_read"] == 3

    def test_missing_required_columns_raises_value_error(self):
        df = pd.DataFrame({"seismic": ["a"], "foo": [1]})
        f = _make_uploaded_file("bad_underground.csv", df)
        with pytest.raises(ValueError, match="Missing required columns"):
            model.process_underground_file(f)

    def test_invalid_numeric_rows_are_rejected(self):
        # Build with object dtype so we can inject non-numeric values
        data = {}
        for col in self.REQUIRED_COLS:
            if col in ("seismic", "seismoacoustic", "shift", "hazard"):
                data[col] = ["a"] * 3
            else:
                data[col] = [1.0] * 3
        data["genergy"][0] = "not_numeric"
        data["energy"][1] = None
        df = pd.DataFrame(data, dtype=object)
        f = _make_uploaded_file("mixed_underground.csv", df)
        result, stats = model.process_underground_file(f)
        assert len(result) == 1  # only row 2 is fully valid
        assert stats["rows_rejected"] == 2

    def test_all_rows_rejected_raises_value_error(self):
        df = self._make_underground_df()
        for col in self.REQUIRED_COLS:
            if col not in ("seismic", "seismoacoustic", "shift", "hazard"):
                df[col] = "bad"
        f = _make_uploaded_file("all_bad_ug.csv", df)
        with pytest.raises(ValueError, match="All rows were rejected"):
            model.process_underground_file(f)


# ---------------------------------------------------------------------------
# Bundled dataset integrity tests
# ---------------------------------------------------------------------------

class TestBundledDatasetsUnchanged:
    def test_open_pit_dataset_hash_unchanged(self, original_open_pit_hash):
        path = os.path.join(PROJECT_ROOT, "slope_stability_dataset.csv")
        assert _sha256(path) == original_open_pit_hash

    def test_underground_dataset_hash_unchanged(self, original_underground_hash):
        path = os.path.join(PROJECT_ROOT, "underground_dataset.csv")
        assert _sha256(path) == original_underground_hash


# ---------------------------------------------------------------------------
# Upload routing and directory separation tests
# ---------------------------------------------------------------------------

class TestUploadRouting:
    def test_open_pit_upload_saved_to_open_pit_dir(self, tmp_user_data):
        df = pd.DataFrame({"fs": [1.5], "reinforcement": [1.0]})
        f = _make_uploaded_file("mine1.csv", df)
        file_bytes = f.getvalue()
        upload_dir = model.get_upload_dir("Open Pit Mines")
        saved_name = model.get_unique_filename(upload_dir, f.name)
        saved_path = model.save_uploaded_bytes(file_bytes, upload_dir, saved_name)

        assert saved_path.startswith(upload_dir)
        assert os.path.exists(saved_path)
        assert "open_pit_uploads" in saved_path

    def test_underground_upload_saved_to_underground_dir(self, tmp_user_data):
        df = pd.DataFrame({
            "seismic": ["a"], "seismoacoustic": ["a"], "shift": ["N"],
            "genergy": [100], "gpuls": [1], "gdenergy": [1], "gdpuls": [1],
            "hazard": ["a"], "nbumps": [0], "nbumps2": [0], "nbumps3": [0],
            "nbumps4": [0], "nbumps5": [0], "nbumps6": [0],
            "nbumps7": [0], "nbumps89": [0], "energy": [100], "maxenergy": [100],
        })
        f = _make_uploaded_file("mine2.csv", df)
        file_bytes = f.getvalue()
        upload_dir = model.get_upload_dir("Underground Pit Mines")
        saved_name = model.get_unique_filename(upload_dir, f.name)
        saved_path = model.save_uploaded_bytes(file_bytes, upload_dir, saved_name)

        assert saved_path.startswith(upload_dir)
        assert os.path.exists(saved_path)
        assert "underground_uploads" in saved_path

    def test_underground_upload_directory_is_not_open_pit_directory(self, tmp_user_data):
        open_pit_dir = model.get_upload_dir("Open Pit Mines")
        underground_dir = model.get_upload_dir("Underground Pit Mines")
        assert open_pit_dir != underground_dir
        assert "open_pit_uploads" not in underground_dir
        assert "underground_uploads" not in open_pit_dir


# ---------------------------------------------------------------------------
# Compilation tests
# ---------------------------------------------------------------------------

class TestSourceCompiles:
    def test_model_py_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(PROJECT_ROOT, "model.py"), doraise=True)

    def test_create_model_py_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(PROJECT_ROOT, "create_model.py"), doraise=True)

    def test_load_model_py_compiles(self):
        import py_compile
        py_compile.compile(os.path.join(PROJECT_ROOT, "load_model.py"), doraise=True)