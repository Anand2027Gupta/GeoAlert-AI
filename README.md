# AI-Based-Rockfall-Prediction-And-Alert-System

AI-powered system for predicting rockfalls and sending real-time alerts in open pit mines using sensor data and machine learning.

## Installation

### Prerequisites

- Python 3.11 (tested with 3.11.9)
- pip (included with Python)

### Setup (Windows PowerShell)

1. Clone the repository and enter the project directory:

   ```powershell
   cd "d:\MahaSena\GeoAlert AI\GeoAlert AI"
   ```

2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install runtime dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. (Optional) Install test dependencies:

   ```powershell
   pip install -r requirements-dev.txt
   ```

### SMTP Configuration (for email notifications)

Email alerts require SMTP configuration. Set these as environment variables or in Streamlit secrets (never hardcode credentials):

- `SMTP_HOST` — SMTP server hostname
- `SMTP_PORT` — SMTP server port (default: 587)
- `SMTP_USER` — SMTP username
- `SMTP_PASSWORD` — SMTP password
- `SMTP_USE_TLS` — Use TLS (default: true)
- `SMTP_FROM_EMAIL` — Sender email address

Example (PowerShell, session-only):

```powershell
$env:SMTP_HOST="smtp.example.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="alerts@example.com"
$env:SMTP_PASSWORD="your-password"
$env:SMTP_FROM_EMAIL="alerts@example.com"
```

For Streamlit secrets, create `.streamlit/secrets.toml` in the project root:

```toml
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "alerts@example.com"
SMTP_PASSWORD = "your-password"
SMTP_USE_TLS = true
SMTP_FROM_EMAIL = "alerts@example.com"
```

### Running the Application

Start the Streamlit app from the project root directory:

```powershell
streamlit run model.py
```

### Running Tests

```powershell
pip install -r requirements-dev.txt
pytest tests/
```

### Model Artifacts

The application loads pre-trained ML models and preprocessing artifacts (`.pkl` files) from the project root. These were trained with scikit-learn 1.7.2. The runtime pins scikit-learn 1.7.2 for artifact compatibility. Do not regenerate or retrain the model artifacts unless explicitly approved.

## Project Phases Summary

### Phase 2: Upload Protection

- Added CSV upload validation with required column checks (`fs`, `reinforcement`)
- Implemented file extension filtering and path traversal protection
- Added file size limits and duplicate detection using UUID-based filenames
- All 26 tests pass

### Phase 3A: Email Notification

- Implemented `send_email()` function using SMTP with TLS support
- Configuration read from environment variables or Streamlit secrets (never hardcoded)
- Recipient addresses parsed from comma-separated input
- Mocked SMTP in tests to prevent external network calls
- All 20 tests pass

### Phase 3B: Underground Preprocessing

- Created `underground_preprocessing.py` with feature-ordered DataFrame preprocessing
- Implemented categorical encoding using saved per-column LabelEncoders
- Added unseen category detection with clear error messages
- Implemented missing value and invalid numeric string handling
- All 15 tests pass

### Phase 4A: Help Desk Attachments

- Added extension validation (.pdf, .jpg, .png)
- Implemented file size limits (configurable)
- Path confinement to prevent directory traversal
- All 22 tests pass

### Phase 4B: Pandas Frequency Deprecation

- Replaced all 5 occurrences of `freq='T'` (deprecated in pandas 2.x) with `freq='min'`
- Updated `model.py` `generate_mock_data()` and `generate_underground_mock_data()` functions
- Verified `freq='T'` raises `ValueError` in pandas 2.x, `freq='min'` is fully compatible
- All 83 tests pass

### Phase 4C: Dependency Version Alignment

- Pinned scikit-learn 1.7.2 (matches artifact training version)
- Updated numpy to `>=2.0,<2.2` for pyarrow/scikit-learn 1.7.2 compatibility
- Updated matplotlib to `>=3.9,<3.10`
- Fixed StandardScaler feature-name warning by passing DataFrame with column names to `scaler.transform()`
- Updated `tests/test_underground_preprocessing.py` to match new preprocessing behavior
- All 83 tests pass with no feature-name warnings

### Phase 5: Final Release-Readiness Audit

- Verified all 83 tests pass in fresh virtual environment
- Confirmed Git hygiene (no tracked venvs, secrets, or user data)
- Audited SMTP configuration (env vars only, no hardcoded credentials)
- Verified documentation accuracy (Python version, venv setup, dependency install, test commands)
- Confirmed model artifact integrity (dataset hashes, unchanged `.pkl` files)
- Identified and resolved StandardScaler feature-name warning
- Finalized commit with 3 file modifications

## Configuration

### Email Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_HOST` | SMTP server hostname | required |
| `SMTP_PORT` | SMTP server port | 587 |
| `SMTP_USER` | SMTP username | required |
| `SMTP_PASSWORD` | SMTP password | required |
| `SMTP_USE_TLS` | Use TLS (true/false) | true |
| `SMTP_FROM_EMAIL` | Sender email address | required |

### Help Desk Attachment Settings

- Allowed extensions: `.pdf`, `.jpg`, `.png`
- Size limit: configurable (currently set in `process_helpdesk_attachment()`)
- Confinement: attachments must reside within allowed directories

## Development Dependencies

- `pytest==8.3.3` — test framework
- Used in conjunction with `requirements.txt` runtime dependencies

## Repository Structure

```
GeoAlert AI/
├── app.py                  # Main Streamlit entry point
├── model.py                # Core application logic (upgraded freq='T' → 'min')
├── underground_preprocessing.py  # Phase 3B/5C preprocessing (fixes scaler warning)
├── notifications.py        # Phase 3A email helper
├── create_model.py         # Model training script
├── load_model.py           # Model loading utilities
├── requirements.txt        # Runtime dependencies (pinned scikit-learn 1.7.2)
├── requirements-dev.txt    # Development dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── user_data/              # User uploads (open_pit_uploads, underground_uploads)
├── helpdesk_attachments/  # Help desk submitted files
├── slope_stability_dataset.csv  # Bundled dataset (read-only)
├── underground_dataset.csv      # Bundled dataset (read-only)
├── *.pkl                   # Model artifacts (underground_rockfall_model, scaler, encoder)
├── tests/
│   ├── test_phase2_uploads.py
│   ├── test_notifications.py
│   ├── test_underground_preprocessing.py
│   └── test_attachments.py
└── *.ipynb               # Jupyter notebooks (training/analysis)

