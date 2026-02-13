# Cybersecurity Anomaly Detection Platform

## Overview
This project is a real-time cybersecurity anomaly detection system using batch processing, streaming, and machine learning to detect suspicious transactions.

---

## Features
- Synthetic data generation with anomaly injection  
- Batch ETL pipeline using Airflow  
- Stream processing using Pub/Sub  
- Isolation Forest ML model  
- FastAPI prediction API  
- Streamlit dashboard visualization  

---

## Architecture
User → Airflow → BigQuery → Pub/Sub → FastAPI → Isolation Forest → Streamlit → Response

---

## Run Instructions

### Install dependencies
pip install -r requirements.txt

### Run API
uvicorn main:app --reload

### Run Dashboard
streamlit run app.py

---

## Team Members
- Rahul Mudanna  
- Madan Kumar  
- Romila Reddy  
- Vaishnavi Gopinath  

---

Data Engineering project demonstrating batch + streaming + ML integration.
