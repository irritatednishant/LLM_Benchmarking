"""
FastAPI Server & REST Telemetry API for the SLM Benchmark Platform.
Provides interactive Swagger UI documentation, live hardware telemetry,
model leaderboard metrics, and real-time inference playground endpoints.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel, Field

from core.config import MODELS, RESULTS_CSV, RESULTS_JSON, TEMPERATURE_RESULTS_CSV
from analytics.metrics import (
    compute_comprehensive_metrics,
    generate_markdown_report,
    get_system_telemetry,
    BENCHMARK_REPORT_MD,
)
from engine.runner import general_prompt, structured_prompt, run_model
from orchestration.benchmark import run_benchmark


app = FastAPI(
    title="SLM Benchmark & Diagnostic Platform API",
    description=(
        "Local Small Language Model (SLM) Evaluation & Telemetry Framework. "
        "Profiles inference latency, generation throughput (tokens/s), RAM/VRAM consumption, "
        "and Pydantic JSON schema compliance across Ollama models."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for external frontend or local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Benchmark execution state
benchmark_job_state = {
    "is_running": False,
    "last_run_timestamp": None,
    "last_status": "Idle",
    "total_evaluated": 0,
    "error": None,
}


class InferenceRequest(BaseModel):
    model: str = Field(default="llama3.2:3b", description="Model identifier in Ollama")
    prompt: str = Field(description="Prompt or customer ticket text to evaluate")
    prompt_type: Literal["structured", "general"] = Field(
        default="structured",
        description="Evaluation mode: 'structured' (Pydantic schema validated) or 'general'",
    )
    temperature: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Sampling temperature")


class InferenceResponse(BaseModel):
    model: str
    prompt: str
    prompt_type: str
    response: str
    parsed: Optional[Any] = None
    valid_json: bool
    latency: float
    generation_time: float
    tokens_per_second: float
    output_tokens: int
    prompt_tokens: int
    memory_mb: Optional[float] = None
    temperature: Optional[float] = None


class BenchmarkRunRequest(BaseModel):
    models: Optional[List[str]] = Field(default=None, description="Subset of models to benchmark")


@app.get("/", include_in_schema=False)
def root():
    """Redirect root access to interactive visual dashboard."""
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard", response_class=HTMLResponse, tags=["Web Dashboard"])
def get_dashboard():
    """Serve the interactive Tailwind CSS and Chart.js telemetry dashboard."""
    template_path = BASE_DIR / "api" / "templates" / "dashboard.html"
    if not template_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard HTML template not found.",
        )
    return HTMLResponse(content=template_path.read_text(encoding="utf-8"))


@app.get("/api/v1/health", tags=["System & Telemetry"])
def get_health() -> Dict[str, Any]:
    """Return host platform specs, RAM capacity, CPU count, and Ollama daemon status."""
    telemetry = get_system_telemetry()
    return {
        "status": "healthy",
        "telemetry": telemetry,
    }


@app.get("/api/v1/models", tags=["System & Telemetry"])
def get_models() -> Dict[str, Any]:
    """Return candidate benchmark models and models currently available in local Ollama."""
    telemetry = get_system_telemetry()
    return {
        "configured_models": MODELS,
        "installed_ollama_models": telemetry.get("installed_models", []),
        "ollama_active": telemetry.get("ollama_running", False),
    }


@app.get("/api/v1/analytics/summary", tags=["Analytics & Leaderboard"])
def get_analytics_summary() -> Dict[str, Any]:
    """
    Fetch comprehensive benchmark analytics, model rankings,
    latency percentiles, and deployment feasibility ratings.
    """
    metrics = compute_comprehensive_metrics()
    if "error" in metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=metrics["error"],
        )
    return metrics


@app.get("/api/v1/analytics/report", tags=["Analytics & Leaderboard"])
def get_diagnostic_report(download: bool = Query(default=False)):
    """
    Export or download the full academic Markdown diagnostic report.
    """
    metrics = compute_comprehensive_metrics()
    if "error" in metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=metrics["error"],
        )

    report_path = generate_markdown_report(metrics)
    if not report_path.exists():
        raise HTTPException(status_code=500, detail="Failed to generate report file.")

    if download:
        return FileResponse(
            path=report_path,
            filename="SLM_BENCHMARK_REPORT.md",
            media_type="text/markdown",
        )

    return PlainTextResponse(content=report_path.read_text(encoding="utf-8"))


@app.post("/api/v1/infer/single", response_model=InferenceResponse, tags=["Live Inference Playground"])
def run_single_inference(payload: InferenceRequest):
    """
    Execute real-time inference on a single prompt or ticket.
    Profiles latency, generation speed, memory, and schema validity on demand.
    """
    try:
        if payload.prompt_type == "structured":
            # Run structured ticket schema validation
            res = structured_prompt(payload.model, payload.prompt)
            res["prompt_type"] = "structured"
            res["model"] = payload.model
            res["prompt"] = payload.prompt
            return res
        else:
            # Run general unconstrained inference
            res = run_model(payload.model, payload.prompt, temperature=payload.temperature)
            res["prompt_type"] = "general"
            res["valid_json"] = True
            res["parsed"] = None
            return res        # Ensure prompt_type is marked
    

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(e)}",
        )


def _execute_benchmark_task(models: Optional[List[str]]):
    """Background task runner for benchmark execution."""
    global benchmark_job_state
    benchmark_job_state["is_running"] = True
    benchmark_job_state["last_status"] = "Running benchmark suite..."
    benchmark_job_state["error"] = None
    try:
        results = run_benchmark(models=models)
        benchmark_job_state["is_running"] = False
        benchmark_job_state["last_status"] = "Completed"
        benchmark_job_state["total_evaluated"] = len(results)
    except Exception as e:
        benchmark_job_state["is_running"] = False
        benchmark_job_state["last_status"] = "Failed"
        benchmark_job_state["error"] = str(e)


@app.post("/api/v1/benchmark/run", tags=["Benchmark Orchestration"])
def trigger_benchmark_run(
    payload: BenchmarkRunRequest,
    background_tasks: BackgroundTasks,
):
    """
    Trigger full benchmark matrix execution in the background.
    """
    global benchmark_job_state
    if benchmark_job_state["is_running"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A benchmark job is already running. Check /api/v1/benchmark/status.",
        )

    background_tasks.add_task(_execute_benchmark_task, payload.models)
    return {
        "status": "queued",
        "message": f"Benchmark job triggered for models: {payload.models or MODELS}",
    }


@app.get("/api/v1/benchmark/status", tags=["Benchmark Orchestration"])
def get_benchmark_job_status():
    """Check execution status of triggered background benchmark runs."""
    return benchmark_job_state

