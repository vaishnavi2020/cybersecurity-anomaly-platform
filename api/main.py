import joblib
import numpy as np
from fastapi import FastAPI
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "anomaly_model.pkl")
scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

@app.post("/predict")
def predict(data: dict):

    features = np.array([[
        data["transactions_last_5min"],
        data["avg_amount"],
        data["high_risk_flag"]
    ]])

    # SCALE INPUT
    scaled_features = scaler.transform(features)

    prediction = model.predict(scaled_features)
    score = model.decision_function(scaled_features)

    return {
        "prediction": "ANOMALY" if prediction[0] == -1 else "NORMAL",
        "anomaly_score": float(abs(score[0]))
    }
