# 📘 **Data Quality Workflow Engine**

A lightweight **FastAPI-based workflow engine** designed for automated data profiling, anomaly detection, rule generation, and iterative data cleaning.

---

# 🔍 **What This Engine Does**

This engine automatically processes datasets by:

- **Profiling numeric columns**
- **Detecting anomalies**, including:
  - Missing values  
  - Negative values  
  - Outliers (IQR or Z-score)
- **Generating cleaning rules**, such as:
  - Median / Mean / Mode imputation
  - Outlier replacement
  - Negative value correction
- **Applying rules until the dataset becomes clean**
- **Supporting branching and loop conditions**
- **Exposing clean REST APIs** for workflow automation

---

# 🧠 **Best Suited For These Types of Datasets**

The engine performs **most efficiently** on:

### ✔ Structured numeric datasets  
CSV-like tabular data.

### ✔ Sensor / IoT datasets  
Examples:  
- temperature  
- humidity  
- voltage  
- pressure  

### ✔ Financial & operational datasets  
Examples:  
- revenue  
- transaction amounts  
- cost metrics  

### ✔ Telemetry / monitoring datasets  
Examples:  
- CPU usage  
- response time  
- memory load  

---

## ❌ **Not Ideal For**

- Text-heavy datasets  
- Images / audio  
- Free-form or unstructured datasets  

---

# 🚀 **API Endpoints**

## **1️⃣ Create Workflow**
Creates a new workflow and returns a **graph_id**.

---

## **2️⃣ Run Workflow**

Runs the workflow with your input dataset and returns:

- Final **cleaned data**
- **Anomaly summary**
- **Rules generated**
- **Execution logs**

---

# ▶ **Running the Project Locally**

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
