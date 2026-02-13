import pandas as pd
import numpy as np
import os

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data")
os.makedirs(data_path, exist_ok=True)

n = 5000

data = pd.DataFrame({
    "txn_count_5min": np.random.poisson(lam=5, size=n),
    "avg_amount_5min": np.random.normal(loc=200, scale=80, size=n),
})

data["high_risk_flag"] = (data["avg_amount_5min"] > 3000).astype(int)

# Inject anomalies
anomalies = pd.DataFrame({
    "txn_count_5min": np.random.randint(20, 50, 150),
    "avg_amount_5min": np.random.randint(2000, 10000, 150),
    "high_risk_flag": 1
})

data = pd.concat([data, anomalies], ignore_index=True)

file_path = os.path.join(data_path, "offline_features.csv")
data.to_csv(file_path, index=False)

print("✅ Dataset created at:", file_path)
