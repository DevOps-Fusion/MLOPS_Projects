from fastapi import FastAPI
from fastapi.responses import FileResponse
import joblib
import pandas as pd
import os


app = FastAPI()

# Load model
model = joblib.load("../model/model.pkl")
vectorizer = joblib.load("../model/vectorizer.pkl")

# Load dataset for detailed response
df = pd.read_csv("../data/devops_issues_dataset.csv")

def normalize(text):
    return text.lower().strip()

@app.get("/")
def home():
    return {"message": "DevOps Issue ML API Running"}

@app.get("/predict")
def predict(issue: str):
    issue_clean = normalize(issue)

    # ML Prediction
    X = vectorizer.transform([issue_clean])
    prediction = model.predict(X)[0]

    # Fetch full details
    row = df[df["category"] == prediction].iloc[0]

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
