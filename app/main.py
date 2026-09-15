from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s"
    )

logger = logging.getLogger(__name__)
APP_ENV = os.getenv("APP_ENV", "development")

def get_environment():
    return APP_ENV

app = FastAPI(
    title="AI Observability Platform",
    version="1.0.0",
)

class TraceResponse(BaseModel):
    trace_id: str
    status: str
    service: str

TRACE_DATA = {
        "abc123": {
        "trace_id": "abc123",
        "status": "completed",
        "service": "ai-observability-platform",
    }
}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>AI Observability Platform</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h1>AI Observability Platform</h1>
            <p>
                Python + FastAPI Backend
            </p>
            <p>
                Open API docs:
                <a href="/docs">/docs</a>
            </p>
        </body>
    </html>
    """


@app.get("/health")
def health_check():
    logger.info(
        "[HEALTH] Health check requested environment=%s",
        APP_ENV)
    return {
        "status": "ok"
    }

@app.get("/config")
def get_config(
    environment: str = Depends(get_environment)
):
    logger.info(
        "[CONFIG] Configuration requested environment=%s",
        environment
    )

    return {
        "environment": environment
    }

@app.get("/traces/{trace_id}", response_model=TraceResponse)
def get_trace(
    trace_id: str = Path(..., min_length=3)):
    logger.info(
        "[TRACE] Lookup attempt trace_id=%s environment=%s",
        trace_id,
        APP_ENV
    )

    trace = TRACE_DATA.get(trace_id)
    if trace is None:
        logger.warning(
            "[TRACE ERROR] Trace not found: %s environment=%s",
            trace_id,
            APP_ENV
        )
        raise HTTPException(
            status_code=404,
            detail="Trace not found"
        )
    logger.info(
        "[TRACE] Trace found: %s environment=%s",
        trace_id,
        APP_ENV
    )
    return trace
