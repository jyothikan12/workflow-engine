Data Quality Workflow Engine

A lightweight FastAPI-based workflow engine designed to automate data profiling, anomaly detection, rule generation, and iterative data cleaning through a node-based graph workflow.

 What This Engine Does

This engine automatically processes datasets by:

Profiling numeric columns

Detecting anomalies such as:

Missing values

Negative values

Outliers (using IQR or Z-Score)

Auto-generating cleaning rules:

Mean / Median / Mode imputation

Outlier replacement

Negative value correction

Applying rules iteratively until the dataset becomes clean

Supporting branching conditions & loops

Exposing simple HTTP APIs to run workflows dynamically

 Best Suited For These Types of Datasets

The engine works most efficiently with:

✔ Structured numeric datasets

Ideal for tabular CSV-like data.

✔ Sensor / IoT datasets

Examples:

temperature

humidity

pressure

voltage

These datasets commonly contain noise and missing values.

✔ Financial & operational datasets

Examples:

transaction amounts

salaries

production values

✔ Telemetry / system monitoring datasets

Examples:

CPU usage

response time

latency

 Not Ideal For

Free-text datasets

Images, audio, or unstructured content

Deeply nested JSON data

API Endpoints
Create Workflow
POST /workflow/create


Creates a new workflow and returns a graph_id.

Run Workflow
POST /workflow/run


Executes the workflow using your input dataset and returns:

Cleaned data

Applied rules

Anomalies detected

Execution logs

▶ Running Locally

Start the FastAPI server:

uvicorn app.main:app --reload


Open interactive API docs:

🔗 http://127.0.0.1:8000/docs

What Could Be Added With More Time

Workflow & run storage in a database

WebSockets for real-time execution logs

Background task support

Visual graph editor for workflows

Custom user-defined nodes via API

Authentication & role-based access
