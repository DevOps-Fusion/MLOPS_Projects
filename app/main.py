#-----------------------------------------------------------------------------------------------------------
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
import joblib
import pandas as pd
import os
import time

# Prometheus imports
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI()

# Load model
model = joblib.load("../model/model.pkl")
vectorizer = joblib.load("../model/vectorizer.pkl")

# Load dataset
df = pd.read_csv("../data/devops_issues_dataset.csv")

def normalize(text):
    return text.lower().strip()

# ✅ Prometheus Metrics
REQUEST_COUNT = Counter('ml_requests_total', 'Total ML Requests')
REQUEST_LATENCY = Histogram('ml_request_latency_seconds', 'Request latency')

# ---------------- ROUTES ---------------- #

@app.get("/")
def home():
    return {"message": "DevOps Issue ML API Running"}

@app.get("/predict")
def predict(issue: str):
    start_time = time.time()

    REQUEST_COUNT.inc()  # count requests

    issue_clean = normalize(issue)

    # ML Prediction
    X = vectorizer.transform([issue_clean])
    prediction = model.predict(X)[0]

    # Fetch details
    row = df[df["category"] == prediction].iloc[0]

    REQUEST_LATENCY.observe(time.time() - start_time)  # record latency

    return {
        "predicted_issue": prediction,
        "description": row["description"],
        "causes": row["causes"],
        "debug": row["debug"],
        "solution": row["solution"]
    }

@app.get("/ui")
def ui():
    return FileResponse(os.path.join("static", "index.html"))

# ✅ IMPORTANT: Metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
