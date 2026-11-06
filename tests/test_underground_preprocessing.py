"""
Phase 3B regression tests: Underground model preprocessing correction.

Tests for underground_preprocessing.py:
- Correct feature names and order (matches training/scaler).
- Correct categorical encoding using saved LabelEncoder mappings.
- Correct numeric scaling using saved StandardScaler.
- Single-row prediction.
- Missing required features.
- Invalid numeric values and missing values.
- Unseen categorical value.
- Missing or incompatible artifacts.
- No row-local category codes used as encoder substitute.

These tests never modify model artifacts or bundled datasets.
They use the real saved artifacts (read-only) where available.
"""

import sys
import os
import warnings
from unittest.mock import patch, MagicMock

import numpy as np
import pandas as pd
import pytest

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import underground_preprocessing as up  # noqa: E402


@pytest.fixture
def artifacts():
    """Load real artifacts (read-only). Returns (model, scaler, encoder)."""
    return up.load_artifacts()


def sample_row():
    """A single valid row matching the underground feature schema."""
    return pd.DataFrame([{
        'seismic': 'a',
        'seismoacoustic': 'a',
        'shift': 'N',
        'genergy': 15000.0,
        'gpuls': 50.0,
        'gdenergy': -70.0,
        'gdpuls': -70.0,
        'hazard': 'a',
        'nbumps': 0,
        'nbumps2': 0,
        'nbumps3': 0,
        'nbumps4': 0,
        'nbumps5': 0,
        'nbumps6': 0,
        'nbumps7': 0,
        'nbumps89': 0,
        'energy': 2000.0,
        'maxenergy': 2000.0,
    }])


class TestFeatureOrder:
    def test_feature_order_matches_scaler(self, artifacts):
        _, scaler, _ = artifacts
        expected = list(scaler.feature_names_in_)
        assert up.UNDERGROUND_FEATURE_ORDER == expected

    def test_feature_count_matches_model(self, artifacts):
        model, _, _ = artifacts
        assert len(up.UNDERGROUND_FEATURE_ORDER) == model.n_features_in_ == 18


class TestCategoricalEncoding:
    def test_known_categories_encoded_correctly(self, artifacts):
        _, scaler, encoder = artifacts
        df = pd.DataFrame([{
            'seismic': 'a', 'seismoacoustic': 'a', 'shift': 'N', 'hazard': 'a',
            'genergy': 1.0, 'gpuls': 1.0, 'gdenergy': 1.0, 'gdpuls': 1.0,
            'nbumps': 1.0, 'nbumps2': 1.0, 'nbumps3': 1.0, 'nbumps4': 1.0,
            'nbumps5': 1.0, 'nbumps6': 1.0, 'nbumps7': 1.0, 'nbumps89': 1.0,
            'energy': 1.0, 'maxenergy': 1.0,
        }])
        encoded = up.encode_categoricals(df, encoder)
        assert encoded['seismic'].iloc[0] == 0
        assert encoded['seismoacoustic'].iloc[0] == 0
        assert encoded['shift'].iloc[0] == 0
        assert encoded['hazard'].iloc[0] == 0

    def test_different_known_category_maps_differently(self, artifacts):
        _, _, encoder = artifacts
        df = pd.DataFrame([{
            'seismic': 'b', 'seismoacoustic': 'c', 'shift': 'W', 'hazard': 'c',
            'genergy': 1.0, 'gpuls': 1.0, 'gdenergy': 1.0, 'gdpuls': 1.0,
            'nbumps': 1.0, 'nbumps2': 1.0, 'nbumps3': 1.0, 'nbumps4': 1.0,
            'nbumps5': 1.0, 'nbumps6': 1.0, 'nbumps7': 1.0, 'nbumps89': 1.0,
            'energy': 1.0, 'maxenergy': 1.0,
        }])
        encoded = up.encode_categoricals(df, encoder)
        assert encoded['seismic'].iloc[0] == 1
        assert encoded['seismoacoustic'].iloc[0] == 2
        assert encoded['shift'].iloc[0] == 1
        assert encoded['hazard'].iloc[0] == 2

    def test_unseen_category_raises_clear_error(self, artifacts):
        _, _, encoder = artifacts
        df = pd.DataFrame([{
            'seismic': 'z',
            'seismoacoustic': 'a', 'shift': 'N', 'hazard': 'a',
            'genergy': 1.0, 'gpuls': 1.0, 'gdenergy': 1.0, 'gdpuls': 1.0,
            'nbumps': 1.0, 'nbumps2': 1.0, 'nbumps3': 1.0, 'nbumps4': 1.0,
            'nbumps5': 1.0, 'nbumps6': 1.0, 'nbumps7': 1.0, 'nbumps89': 1.0,
            'energy': 1.0, 'maxenergy': 1.0,
        }])
        with pytest.raises(ValueError, match="Unseen category"):
            up.encode_categoricals(df, encoder)

    def test_not_row_local_codes(self, artifacts):
        _, _, encoder = artifacts
        df = pd.DataFrame([{
            'seismic': 'b', 'seismoacoustic': 'a', 'shift': 'N', 'hazard': 'a',
            'genergy': 1.0, 'gpuls': 1.0, 'gdenergy': 1.0, 'gdpuls': 1.0,
            'nbumps': 1.0, 'nbumps2': 1.0, 'nbumps3': 1.0, 'nbumps4': 1.0,
            'nbumps5': 1.0, 'nbumps6': 1.0, 'nbumps7': 1.0, 'nbumps89': 1.0,
            'energy': 1.0, 'maxenergy': 1.0,
        }])
        encoded = up.encode_categoricals(df, encoder)
        assert encoded['seismic'].iloc[0] == 1


class TestScaling:
    def test_scaler_applied_to_all_features(self, artifacts):
        _, scaler, encoder = artifacts
        df = pd.DataFrame([{
            'seismic': 'a', 'seismoacoustic': 'a', 'shift': 'N', 'hazard': 'a',
            'genergy': 15000.0, 'gpuls': 50.0, 'gdenergy': -70.0, 'gdpuls': -70.0,
            'nbumps': 0, 'nbumps2': 0, 'nbumps3': 0, 'nbumps4': 0,
            'nbumps5': 0, 'nbumps6': 0, 'nbumps7': 0, 'nbumps89': 0,
            'energy': 2000.0, 'maxenergy': 2000.0,
        }])
        encoded = up.encode_categoricals(df, encoder)
        # Reorder columns to match the scaler's expected feature names order,
        # matching the fix in preprocess_input: encoded[scaler.feature_names_in_]
        encoded = encoded[scaler.feature_names_in_]
        scaled = scaler.transform(encoded.astype(float))
        assert scaled.shape == (1, 18)
        assert np.all(np.isfinite(scaled))

    def test_preprocess_input_returns_correct_shape(self, artifacts):
        model, scaler, encoder = artifacts
        X = up.preprocess_input(sample_row(), model, scaler, encoder)
        assert X.shape == (1, 18)


class TestMissingInvalid:
    def test_missing_features_raises(self, artifacts):
        model, scaler, encoder = artifacts
        df = pd.DataFrame([{'seismic': 'a'}])
        with pytest.raises(ValueError, match="Missing required underground features"):
            up.preprocess_input(df, model, scaler, encoder)

    def test_nan_numeric_propagates(self, artifacts):
        model, scaler, encoder = artifacts
        df = sample_row().copy()
        df.loc[0, 'genergy'] = np.nan
        X = up.preprocess_input(df, model, scaler, encoder)
        assert np.isnan(X).any(), "Expected NaN to propagate through scaling"

    def test_invalid_numeric_string_raises(self, artifacts):
        model, scaler, encoder = artifacts
        df = pd.DataFrame([{
            'seismic': 'a', 'seismoacoustic': 'a', 'shift': 'N', 'hazard': 'a',
            'genergy': 'not_a_number', 'gpuls': 50.0, 'gdenergy': -70.0, 'gdpuls': -70.0,
            'nbumps': 0, 'nbumps2': 0, 'nbumps3': 0, 'nbumps4': 0,
            'nbumps5': 0, 'nbumps6': 0, 'nbumps7': 0, 'nbumps89': 0,
            'energy': 2000.0, 'maxenergy': 2000.0,
        }], dtype=object)
        with pytest.raises((ValueError, TypeError)):
            up.preprocess_input(df, model, scaler, encoder)


class TestPrediction:
    def test_single_row_prediction_returns_array(self, artifacts):
        model, scaler, encoder = artifacts
        preds = up.predict(sample_row(), model, scaler, encoder)
        assert isinstance(preds, np.ndarray)
        assert preds.shape == (1,)
        assert preds[0] in (0, 1)

    def test_predict_without_artifacts_loads_from_disk(self):
        preds = up.predict(sample_row())
        assert isinstance(preds, np.ndarray)
        assert preds.shape == (1,)
        assert preds[0] in (0, 1)


class TestArtifacts:
    def test_load_artifacts_returns_trio(self):
        model, scaler, encoder = up.load_artifacts()
        assert model is not None
        assert scaler is not None
        assert encoder is not None
        assert isinstance(encoder, dict)
        assert set(encoder.keys()) == set(up.CATEGORICAL_COLS)

    def test_missing_artifact_file_raises(self, monkeypatch):
        monkeypatch.setattr(up, "ARTIFACT_DIR", "/nonexistent/path")
        with pytest.raises(FileNotFoundError):
            up.load_artifacts()