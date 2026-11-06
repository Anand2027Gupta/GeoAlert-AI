"""Pydantic schemas for GeoAlert AI API."""
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import numpy as np


class OpenPitInput(BaseModel):
    """Input features for open-pit inference."""
    fs: float = Field(
        ..., ge=1.0, le=3.0,
        description="Factor of safety (verified range from training: 1.0-3.0)"
    )
    reinforcement: float = Field(
        ..., ge=0.0, le=5.0,
        description="Reinforcement amount (verified range from training: 0.0-5.0)"
    )
    
    @validator("fs", "reinforcement")
    def validate_finite(cls, v):
        """Reject NaN and infinity."""
        if not np.isfinite(v):
            raise ValueError(f"{v} is not a finite number")
        return v


class UndergroundInput(BaseModel):
    """Input features for underground inference (18 features)."""
    seismic: float
    seismoacoustic: float
    shift: float
    genergy: float
    gpuls: float
    gdenergy: float
    gdpuls: float
    hazard: float
    nbumps: float
    nbumps2: float
    nbumps3: float
    nbumps4: float
    nbumps5: float
    nbumps6: float
    nbumps7: float
    nbumps89: float
    energy: float
    maxenergy: float


class PredictRequest(BaseModel):
    """Request discriminator for mine type."""
    mine_type: Literal["open-pit", "underground"] = Field(
        ..., description="Type of mine inference to perform"
    )
    open_pit: Optional[OpenPitInput] = Field(
        None, description="Open-pit features (fs, reinforcement)"
    )
    underground: Optional[UndergroundInput] = Field(
        None, description="Underground 18-feature vector"
    )


class PredictResponse(BaseModel):
    """Response from prediction endpoint."""
    risk: int = Field(..., ge=0, le=1, description="0 = stable, 1 = high risk")
    risk_level: Literal["Low", "High"] = Field(..., description="Human-readable risk level")
    message: str = Field(..., description="Human-readable explanation")
    mine_type: str = Field(..., description="Type of inference performed")


class CSVUpload(BaseModel):
    """CSV upload request."""
    mine_type: Literal["open-pit", "underground"] = Field(
        ..., description="Type of mine for inference"
    )
    file_bytes: bytes = Field(..., description="Uploaded CSV file bytes")


class NotifyRequest(BaseModel):
    """Notification request (no actual email sent)."""
    subject: str = Field(..., description="Email subject line")
    message: str = Field(..., description="Email body message")
    to_emails: str = Field(
        ..., description="Comma-separated recipient email addresses"
    )


class HealthResponse(BaseModel):
    """Health check response."""
    status: Literal["healthy", "unhealthy"] = Field(..., description="Overall status")
    services: dict = Field(
        default_factory=dict,
        description="Service availability status"
    )