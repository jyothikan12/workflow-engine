Data Quality Workflow Engine

A FastAPI-powered workflow engine that:

Profiles data

Detects anomalies

Generates rules (imputation, outlier fixes, negative fixes)

Applies rules until data becomes clean

Supports branching and loop conditions

Provides workflow creation and execution APIs

API Endpoints
Create Workflow

POST /workflow/create
Creates a new data quality workflow and returns a graph_id.

Run Workflow

POST /workflow/run
Runs the workflow using your input data and returns:

Final cleaned data

Anomaly summary

Rules applied

Execution logs

Running Locally
uvicorn app.main:app --reload


Once running, you can open interactive docs:

🔗 http://127.0.0.1:8000/docs

Project Structure
app/
  ├── main.py                # FastAPI entrypoint
  ├── engine/
  │     ├── runner.py        # Graph runner (state → transitions → loop)
  │     └── registry.py      # Node registry
  ├── registry/
  │     └── tools.py         # Profiling, anomaly detection, rule generation
  └── workflows/
        └── data_quality.py  # Example workflow

What the Workflow Engine Supports

Node-based workflow execution

Shared state passed between nodes

Looping until anomalies = 0

Conditional branching

Missing-value detection + imputation

Negative-value detection + fix

Outlier detection (IQR or Z-score)

Auto rule generation + application

Clean and simple HTTP API

Future Improvements (If More Time Is Available)

Store workflow definitions & runs in a database

WebSockets for live workflow logs

Background tasks for long-running workflows

Graph visualization UI

Allow user-created custom nodes via API

Authentication & multi-user workflow isolation
