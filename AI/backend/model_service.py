"""Model service for GeoAlert AI inference."""
import joblib
import os
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent
ARTIFACTS_DIR = Path(__file__).resolve().parents[2]

_open_pit_model = None
_open_pit_loaded = False


def get_open_pit_model():
    global _open_pit_model, _open_pit_loaded
    if _open_pit_model is None:
        model_path = ARTIFACTS_DIR / "rockfall_model_fs_reinforcement.pkl"
        if not model_path.exists():
            raise FileNotFoundError(f"Open-pit model not found at {model_path}")
        _open_pit_model = joblib.load(model_path)
        _open_pit_loaded = True
    return _open_pit_model


def predict_open_pit(fs: float, reinforcement: float) -> dict:
    """Run open-pit inference.
    
    Verified inputs:
    - fs: float, factor of safety (verified range: 1.0-3.0 from create_model.py)
    - reinforcement: float, reinforcement amount (verified range: 0.0-5.0 from create_model.py)
    
    Returns:
        dict with keys: risk (0=stable, 1=high risk), risk_level ("Low"|"High"), message (str)
    """
    try:
        model = get_open_pit_model()
        import pandas as pd
        df = pd.DataFrame({"fs": [fs], "reinforcement": [reinforcement]})
        # Apply same column normalization as process_uploaded_file()
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        rename_map = {"factor_of_safety_fs": "fs", "reinforcement_numeric": "reinforcement"}
        for orig in rename_map:
            if orig in df.columns:
                df.rename(columns={orig: rename_map[orig]}, inplace=True)
        prediction = model.predict(df)[0]
        risk = int(prediction)
        risk_level = "Low" if risk == 0 else "High"
        message = (
            f"Open-pit stability {'assessed as stable' if risk == 0 else 'assessed as high risk'}. "
            f"Factor of Safety: {fs:.2f}, Reinforcement: {reinforcement:.2f}."
        )
        return {"risk": risk, "risk_level": risk_level, "message": message}
    except Exception as e:
        return {"risk": None, "risk_level": "Error", "message": f"Inference failed: {str(e)[:100]}"}