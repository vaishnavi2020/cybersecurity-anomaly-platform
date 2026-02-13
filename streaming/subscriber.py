# from google.cloud import pubsub_v1
# import json
# import requests

# project_id = "cyber-security-de2-487020"
# subscription_id = "cyber-sub"

# subscriber = pubsub_v1.SubscriberClient()
# subscription_path = subscriber.subscription_path(project_id, subscription_id)

# def callback(message):
#     data = json.loads(message.data.decode("utf-8"))
#     print("Received:", data)

#     # Send to FastAPI model
#     response = requests.post(
#         "http://127.0.0.1:8000/predict",
#         headers={"x-api-key": "my_secure_key"},
#         json=data
#     )

#     print("Prediction:", response.json())

#     message.ack()

# subscriber.subscribe(subscription_path, callback=callback)

# print("Listening for messages...")

# import time
# while True:
#     time.sleep(60)
import json
import requests
import smtplib
from email.mime.text import MIMEText
from google.cloud import pubsub_v1
from google.cloud import bigquery
import os

project_id = "cyber-security-de2-487020"
subscription_id = "login-events-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

bq_client = bigquery.Client()
table_id = "cyber-security-de2-487020.cyber_dataset.raw_logs"

blocked_users = set()


def send_email(user_id, score):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    receiver = "your_email@gmail.com"

    msg = MIMEText(f"🚨 Anomaly Detected!\nUser: {user_id}\nScore: {score}")
    msg["Subject"] = "Cyber Attack Alert"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def callback(message):
    data = json.loads(message.data.decode("utf-8"))

    # Insert into BigQuery
    rows = [{
        "event_time": data["timestamp"],
        "user_id": data["user_id"],
        "event_type": data["event_type"],
        "country": data["country"]
    }]
    bq_client.insert_rows_json(table_id, rows)

    # Aggregate features
    total_events = 1
    failed_logins = 1 if data["event_type"] == "login_fail" else 0
    failure_rate = failed_logins / total_events

    # Call API
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={
            "total_events": total_events,
            "failed_logins": failed_logins,
            "failure_rate": failure_rate
        }
    )

    result = response.json()

    if result["is_anomaly"] == 1:
        print(f"🚫 Blocking user {data['user_id']}")
        blocked_users.add(data["user_id"])
        send_email(data["user_id"], result["anomaly_score"])

    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

print("Listening for messages...")
streaming_pull_future.result()
