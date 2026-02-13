# import pandas as pd
# import numpy as np
# import joblib
# import os
# import matplotlib.pyplot as plt
# from sklearn.ensemble import IsolationForest
# from sklearn.preprocessing import StandardScaler

# # Paths
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# data_path = os.path.join(BASE_DIR, "data", "offline_features.csv")
# model_path = os.path.join(BASE_DIR, "models")
# results_path = os.path.join(BASE_DIR, "results")

# os.makedirs(model_path, exist_ok=True)
# os.makedirs(results_path, exist_ok=True)

# # Load data
# df = pd.read_csv(data_path)

# features = ["txn_count_5min", "avg_amount_5min", "high_risk_flag"]
# X = df[features]

# # Scaling
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # -----------------------------
# # Contamination Sensitivity Test
# # -----------------------------
# print("\n=== Contamination Sensitivity Analysis ===\n")

# for contamination in [0.01, 0.02, 0.05]:
#     model = IsolationForest(
#         n_estimators=300,
#         contamination=contamination,
#         random_state=42
#     )
#     model.fit(X_scaled)
#     preds = model.predict(X_scaled)
    
#     anomaly_percent = np.mean(preds == -1) * 100
    
#     print(f"Contamination: {contamination}")
#     print(f"Detected anomalies: {anomaly_percent:.2f}%")
#     print("-" * 40)

# # -----------------------------
# # Final Model (Chosen 0.02)
# # -----------------------------
# model = IsolationForest(
#     n_estimators=300,
#     contamination=0.02,
#     random_state=42
# )

# model.fit(X_scaled)

# # Predictions
# scores = model.decision_function(X_scaled)
# predictions = model.predict(X_scaled)

# df["anomaly_score"] = scores
# df["is_anomaly"] = predictions

# # Save model
# joblib.dump(model, os.path.join(model_path, "anomaly_model.pkl"))
# joblib.dump(scaler, os.path.join(model_path, "scaler.pkl"))

# # -----------------------------
# # Evaluation Metrics
# # -----------------------------
# print("\n=== Final Model Evaluation ===\n")

# total_records = len(df)
# total_anomalies = np.sum(predictions == -1)
# percent_anomalies = np.mean(predictions == -1) * 100

# print("Total records:", total_records)
# print("Anomalies detected:", total_anomalies)
# print("Percentage anomalies:", percent_anomalies)

# # -----------------------------
# # Feature Comparison
# # -----------------------------
# print("\n=== Feature Analysis ===\n")

# for feature in features:
#     normal_mean = df[df["is_anomaly"] == 1][feature].mean()
#     anomaly_mean = df[df["is_anomaly"] == -1][feature].mean()
    
#     print(f"{feature}:")
#     print(f"   Normal Mean: {normal_mean:.2f}")
#     print(f"   Anomaly Mean: {anomaly_mean:.2f}")
#     print("-" * 40)

# # -----------------------------
# # Save Histogram
# # -----------------------------
# plt.figure(figsize=(8,5))
# plt.hist(scores, bins=50)
# plt.title("Isolation Forest Anomaly Score Distribution")
# plt.xlabel("Anomaly Score")
# plt.ylabel("Frequency")
# plt.tight_layout()
# plt.savefig(os.path.join(results_path, "anomaly_score_distribution.png"))
# plt.close()

# print("\n📊 Histogram saved in results folder.")
# print("✅ Model training and evaluation complete.")
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Simulated training data
data = pd.DataFrame({
    "total_events": np.random.randint(1, 50, 1000),
    "failed_logins": np.random.randint(0, 10, 1000)
})

data["failure_rate"] = data["failed_logins"] / data["total_events"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

model = IsolationForest(contamination=0.05)
model.fit(X_scaled)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/anomaly_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("Model trained and saved.")
