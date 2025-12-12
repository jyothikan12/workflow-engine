from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from app.workflows.data_quality import create_data_quality_workflow
from app.engine.runner import run_graph

app = FastAPI()

GRAPH_RUN_HISTORY: Dict[str, Any] = {}


class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


@app.post("/workflow/create")
def create_workflow():
    graph_id = create_data_quality_workflow()
    return {"graph_id": graph_id, "message": "Data Quality Workflow Created"}


@app.post("/workflow/run")
def run_workflow(req: RunRequest):
    run_id = str(uuid.uuid4())
    GRAPH_RUN_HISTORY[run_id] = {"status": "running", "state": req.initial_state}

    result = run_graph(req.graph_id, req.initial_state)

    GRAPH_RUN_HISTORY[run_id] = {
        "status": "completed",
        "state": result.get("final_state", {}),
        "logs": result.get("logs", [])
    }

    return {
        "run_id": run_id,
        "final_state": result.get("final_state"),
        "logs": result.get("logs")
    }


@app.get("/workflow/state/{run_id}")
def get_workflow_state(run_id: str):
    return GRAPH_RUN_HISTORY.get(run_id, {"error": "Run ID not found"})


@app.get("/")
def home():
    return {"message": "Workflow Engine is Running!"}
