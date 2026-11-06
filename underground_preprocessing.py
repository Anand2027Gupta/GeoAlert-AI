"""
Underground rockfall model preprocessing helper.

Applies the same preprocessing used during training:
1. Reorders columns to match the training feature order.
2. Encodes categorical columns using the saved per-column LabelEncoders.
3. Scales all features using the saved StandardScaler.

Never uses row-local category codes as a substitute for the saved encoder.
"""

import os
import pickle
from typing import List, Tuple, Optional

import numpy as np
import pandas as pd

# Exact feature order from training (matches underground_scaler.pkl feature_names_in_)
UNDERGROUND_FEATURE_ORDER: List[str] = [
    'seismic', 'seismoacoustic', 'shift', 'genergy', 'gpuls', 'gdenergy',
    'gdpuls', 'hazard', 'nbumps', 'nbumps2', 'nbumps3', 'nbumps4',
    'nbumps5', 'nbumps6', 'nbumps7', 'nbumps89', 'energy', 'maxenergy'
]

CATEGORICAL_COLS: List[str] = ['seismic', 'seismoacoustic', 'shift', 'hazard']

ARTIFACT_DIR = os.path.dirname(os.path.abspath(__file__))


def _artifact_path(name: str) -> str:
    return os.path.join(ARTIFACT_DIR, name)


def load_artifacts() -> Tuple:
    """Load the saved model, scaler, and encoder artifacts.

    Returns
    -------
    (model, scaler, encoder) tuple.
    """
    with open(_artifact_path("underground_rockfall_model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(_artifact_path("underground_scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    with open(_artifact_path("underground_encoder.pkl"), "rb") as f:
        encoder = pickle.load(f)
    return model, scaler, encoder


def validate_features(df: pd.DataFrame) -> List[str]:
    """Return list of missing required features."""
    return [col for col in UNDERGROUND_FEATURE_ORDER if col not in df.columns]


def encode_categoricals(df: pd.DataFrame, encoder: dict) -> pd.DataFrame:
    """Encode categorical columns using saved per-column LabelEncoders.

    Raises ValueError with a clear message if an unseen category is found.
    """
    result = df.copy()
    for col in CATEGORICAL_COLS:
        le = encoder[col]
        values = result[col].astype(str).tolist()
        try:
            result[col] = le.transform(values)
        except ValueError as exc:
            # LabelEncoder.transform raises on unseen categories.
            # Report explicitly rather than silently substituting a code.
            seen = set(le.classes_)
            unseen = sorted(set(values) - seen)
            raise ValueError(
                f"Unseen category value(s) in column '{col}': {unseen}. "
                f"Known categories: {sorted(seen)}"
            ) from exc
    return result


def preprocess_input(df: pd.DataFrame, model=None, scaler=None, encoder=None) -> np.ndarray:
    """Preprocess a DataFrame of underground monitoring data for model inference.

    Parameters
    ----------
    df : pd.DataFrame
        Raw input with the 18 underground features.
    model, scaler, encoder : optional
        Pre-loaded artifacts. If None, they are loaded from disk.

    Returns
    -------
    np.ndarray
        Scaled, encoded feature matrix ready for model.predict().
        Shape: (n_rows, 18).

    Raises
    ------
    ValueError
        If required features are missing, values are invalid, or unseen
        categorical values are encountered.
    """
    missing = validate_features(df)
    if missing:
        raise ValueError(f"Missing required underground features: {missing}")

    # Select and reorder columns to match training/scaler order exactly.
    ordered = df[UNDERGROUND_FEATURE_ORDER].copy()

    # Load artifacts if not provided.
    if model is None or scaler is None or encoder is None:
        model, scaler, encoder = load_artifacts()

    # Encode categorical columns using saved LabelEncoders.
    encoded = encode_categoricals(ordered, encoder)

    # Reorder columns to match the scaler's expected feature names order.
    # The scaler was fitted on a DataFrame with feature_names_in_ in a specific
    # order (categorical columns interspersed with numeric). Passing a plain
    # NumPy array via .values would lose this ordering, so we reindex explicitly.
    encoded = encoded[scaler.feature_names_in_]

    # Apply the saved StandardScaler (trained on all 18 encoded features).
    scaled = scaler.transform(encoded.astype(float))

    return scaled


def predict(df: pd.DataFrame, model=None, scaler=None, encoder=None) -> np.ndarray:
    """Run underground rockfall prediction on preprocessed input.

    Returns
    -------
    np.ndarray
        Model predictions (0 = Safe, 1 = High Risk).
    """
    if model is None:
        model, scaler, encoder = load_artifacts()
    X = preprocess_input(df, model=model, scaler=scaler, encoder=encoder)
    return model.predict(X)