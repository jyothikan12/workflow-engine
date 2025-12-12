# Data Quality Workflow Engine

A FastAPI-powered workflow engine that:

- Profiles data
- Detects anomalies
- Generates rules (imputation, outlier fixes, negative fixes)
- Applies rules until data is clean
- Supports branching and loop conditions
- Provides workflow creation and execution APIs

## API Endpoints

### Create Workflow

POST /workflow/create  
Creates a new data quality workflow.

### Run Workflow

POST /workflow/run  
Runs the workflow with your input data.

---

## Running Locally

```bash
uvicorn app.main:app --reload
```
