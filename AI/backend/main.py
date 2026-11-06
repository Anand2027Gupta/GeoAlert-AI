"""FastAPI backend for GeoAlert AI."""

import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .schemas import (
    HealthResponse,
    PredictRequest,
    PredictResponse,
    CSVUpload,
    NotifyRequest,
    OpenPitInput,
    UndergroundInput,
)
from .model_service import predict_open_pit

logger = logging.getLogger(__name__)

app = FastAPI(
    title="GeoAlert AI API",
    version="0.1.0",
    description="API for geotechnical rockfall risk inference",
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint.
    
    Returns truthful status about API process and model availability.
    """
    services = {}
    
    # Check open-pit model availability
    try:
        from .model_service import get_open_pit_model
        model = get_open_pit_model()
        services["open_pit_model"] = "loaded"
    except Exception as e:
        logger.warning(f"Open-pit model not available: {e}")
        services["open_pit_model"] = "unavailable"
    
    # Determine overall status
    all_loaded = all(
        s == "loaded" for s in services.values()
    )
    status = "healthy" if all_loaded else "unhealthy"
    
    return HealthResponse(status=status, services=services)


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """Predict endpoint for geo-risk inference.
    
    Supports open-pit and underground mine types.
    Returns truthful results or clear error messages.
    """
    try:
        if request.mine_type == "open-pit":
            if request.open_pit is None:
                raise HTTPException(
                    status_code=400,
                    detail="open-pit features (fs, reinforcement) are required",
                )
            result = predict_open_pit(request.open_pit.fs, request.open_pit.reinforcement)
            if result["risk"] is None:
                raise HTTPException(
                    status_code=500,
                    detail=result["message"],
                )
            return PredictResponse(
                risk=result["risk"],
                risk_level=result["risk_level"],
                message=result["message"],
                mine_type="open-pit",
            )
        
        elif request.mine_type == "underground":
            # Not implemented in this phase
            raise HTTPException(
                status_code=501,
                detail="Underground inference not yet implemented in this phase",
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported mine type: {request.mine_type}",
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)[:200]}",
        )


@app.post("/predict/csv", response_model=PredictResponse)
async def predict_csv(upload: CSVUpload):
    """CSV upload endpoint for batch inference.
    
    Currently supports open-pit inference only via CSV with 'fs' and 'reinforcement' columns.
    """
    try:
        import pandas as pd
        import io
        
        df = pd.read_csv(io.BytesIO(upload.file_bytes))
        
        # Normalize columns same as process_uploaded_file()
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        rename_map = {"factor_of_safety_fs": "fs", "reinforcement_numeric": "reinforcement"}
        for orig in rename_map:
            if orig in df.columns:
                df.rename(columns={orig: rename_map[orig]}, inplace=True)
        
        # Check for required columns
        if "fs" not in df.columns or "reinforcement" not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'fs' and 'reinforcement' columns for open-pit inference",
            )
        
        # Take first row for single prediction
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        row = df.iloc[0]
        fs = float(row["fs"])
        reinforcement = float(row["reinforcement"])
        
        result = predict_open_pit(fs, reinforcement)
        
        if result["risk"] is None:
            raise HTTPException(status_code=500, detail=result["message"])
        
        return PredictResponse(
            risk=result["risk"],
            risk_level=result["risk_level"],
            message=result["message"],
            mine_type="open-pit",
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CSV prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"CSV prediction failed: {str(e)[:200]}")


@app.post("/notify", response_model=dict)
async def notify(request: NotifyRequest):
    """Notification endpoint (simulated - no actual email sent).
    
    Returns a status indicating the notification was simulated.
    """
    return {
        "success": False,
        "message": "Email notification simulated - no actual email sent. Configure SMTP settings to enable real email.",
        "requested_subject": request.subject,
        "requested_recipients": request.to_emails,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)