import json
import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="KKBox Churn Prediction API")

model = joblib.load("models/churn_model.pkl")
features = json.load(open("models/features.json"))

@app.get("/")
def home():
    return {"message": "Churn prediction API is running"}

@app.post("/predict")
def predict(customer: dict):
    row = pd.DataFrame([customer]).reindex(columns=features).astype(float)
    risk = float(model.predict_proba(row)[:, 1][0])
    return {"churn_risk": round(risk, 4), "high_risk": risk > 0.5}