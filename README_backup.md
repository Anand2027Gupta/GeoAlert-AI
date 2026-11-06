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

- `SMTP_HOST` â€” SMTP server hostname
- `SMTP_PORT` â€” SMTP server port (default: 587)
- `SMTP_USER` â€” SMTP username
- `SMTP_PASSWORD` â€” SMTP password
- `SMTP_USE_TLS` â€” Use TLS (default: true)
- `SMTP_FROM_EMAIL` â€” Sender email address

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

### Known Limitations

- Underground model artifacts were pickled with scikit-learn 1.7.2; loading with a different scikit-learn version emits version warnings but does not prevent inference.

