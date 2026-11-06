"""
conftest for tests.

Sets up a lightweight Streamlit mock so importing model.py does not
require a Streamlit script-run context.
"""

import sys
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# Streamlit mock: file_uploader returns None (no upload at import time)
# ---------------------------------------------------------------------------
_st = MagicMock()
_st.sidebar.file_uploader.return_value = None
_st.sidebar.radio.return_value = "Open Pit Mines"
sys.modules["streamlit"] = _st