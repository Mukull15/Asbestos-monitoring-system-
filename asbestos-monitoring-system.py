"""
Asbestos Monitoring System for Sugar Mill Industry
---------------------------------------------------
This application monitors asbestos levels in sugar mills using IoT sensors,
processes the data through Kafka for real-time analysis, and provides
alerts and visualizations through a web dashboard.
"""

# Required dependencies:
# pip install kafka-python fastapi uvicorn pydantic numpy pandas scikit-learn python-dotenv dash plotly

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks, HTTPException
from kafka import KafkaProducer, KafkaConsumer
from sklearn.ensemble import IsolationForest

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("asbestos_monitoring.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("asbestos_monitoring")

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
SENSOR_TOPIC = os.getenv("SENSOR_TOPIC", "asbestos-sensor-data")
ALERT_TOPIC = os.getenv("ALERT_TOPIC", "asbestos-alerts")
ANALYSIS_TOPIC = os.getenv("ANALYSIS_TOPIC", "asbestos-analysis")

# Asbestos safety thresholds (fibers per cubic centimeter)
SAFE_THRESHOLD = 0.1  # Safe level
WARNING_THRESHOLD = 0.5  # Warning level
DANGER_THRESHOLD = 1.0  # Danger level - requires immediate action

# API models
class SensorReading(BaseModel):
    sensor_id: str
    location: str
    timestamp: Optional[datetime] = None
    asbestos_level: float
    temperature: float
    humidity: float
    pressure: float
    
class AlertMessage(BaseModel):
    sensor_id: str
    location: str
    timestamp: datetime
    asbestos_level: float
    severity: str
    message: str

class AnalysisResult(BaseModel):
    timestamp: datetime
    location: str
    average_level: float
    trend: str
    anomaly_score: float
    prediction: float

# Initialize FastAPI
app = FastAPI(title="Asbestos Monitoring System API")

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sensor data storage (in-memory for this example, use a database in production)
sensor_readings = []
alerts = []
analysis_results = []

# Anomaly detection model
model = IsolationForest(contamination=0.05, random_state=42)
model_trained = False

def process_sensor_data(sensor_data):
    """Process incoming sensor data and publish to Kafka"""
    if not sensor_data.timestamp:
        sensor_data.timestamp = datetime.now()
    
    # Send to Kafka topic
    producer.send(
        SENSOR_TOPIC, 
        sensor_data.dict()
    )
    
    # Store reading (would use a database in production)
    sensor_readings.append(sensor_data.dict())
    logger.info(f"Processed sensor reading from {sensor_data.sensor_id} at {sensor_data.location}")
    
    # Check for threshold violations
    check_thresholds(sensor_data)

def check_thresholds(sensor_data):
    """Check if sensor reading exceeds safety thresholds"""
    alert = None
    
    if sensor_data.asbestos_level >= DANGER_THRESHOLD:
        alert = AlertMessage(
            sensor_id=sensor_data.sensor_id,
            location=sensor_data.location,
            timestamp=sensor_data.timestamp,
            asbestos_level=sensor_data.asbestos_level,
            severity="DANGER",
            message=f"DANGER: Asbestos level ({sensor_data.asbestos_level}) exceeds safety limit. Immediate evacuation required."
        )
    elif sensor_data.asbestos_level >= WARNING_THRESHOLD:
        alert = AlertMessage(
            sensor_id=sensor_data.sensor_id,
            location=sensor_data.location,
            timestamp=sensor_data.timestamp,
            asbestos_level=sensor_data.asbestos_level,
            severity="WARNING",
            message=f"WARNING: Elevated asbestos level ({sensor_data.asbestos_level}) detected. Investigate immediately."
        )
    
    if alert:
        # Send alert to Kafka
        producer.send(ALERT_TOPIC, alert.dict())
        alerts.append(alert.dict())
        logger.warning(f"Alert generated: {alert.severity} - {alert.message}")

async def start_kafka_consumer(background_tasks: BackgroundTasks):
    """Start Kafka consumer to process incoming sensor data"""
    consumer = KafkaConsumer(
        SENSOR_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    
    background_tasks.add_task(consume_kafka_messages, consumer)
    logger.info("Kafka consumer started")

async def consume_kafka_messages(consumer):
    """Consume messages from Kafka and process them"""
    for message in consumer:
        data = message.value
        perform_analysis(data)

def perform_analysis(data):
    """Perform real-time analysis on sensor data"""
    global model_trained
    
    # Convert current data point to features for analysis
    features = np.array([[
        data['asbestos_level'],
        data['temperature'],
        data['humidity'],
        data['pressure']
    ]])
    
    # Get recent readings from this location
    location_readings = [r for r in sensor_readings 
                         if r['location'] == data['location']]
    
    # If we have enough data, train or use the model
    if len(location_readings) >= 50:
        if not model_trained:
            # Train model on historical data
            train_data = np.array([
                [r['asbestos_level'], r['temperature'], r['humidity'], r['pressure']]
                for r in location_readings[-100:]
            ])
            model.fit(train_data)
            model_trained = True
        
        # Detect anomalies
        anomaly_score = model.decision_function(features)[0]
        
        # Calculate trend (simple approach for demo)
        recent_readings = location_readings[-10:]
        if len(recent_readings) >= 5:
            avg_recent = sum(r['asbestos_level'] for r in recent_readings[-5:]) / 5
            avg_previous = sum(r['asbestos_level'] for r in recent_readings[:-5]) / (len(recent_readings) - 5)
            
            if avg_recent > avg_previous * 1.1:
                trend = "increasing"
            elif avg_recent < avg_previous * 0.9:
                trend = "decreasing"
            else:
                trend = "stable"
        else:
            trend = "insufficient data"
        
        # Simple prediction (average of last 3 readings)
        prediction = sum(r['asbestos_level'] for r in recent_readings[-3:]) / 3 if len(recent_readings) >= 3 else data['asbestos_level']
        
        # Create analysis result
        analysis = AnalysisResult(
            timestamp=datetime.now(),
            location=data['location'],
            average_level=sum(r['asbestos_level'] for r in recent_readings) / len(recent_readings),
            trend=trend,
            anomaly_score=float(anomaly_score),
            prediction=float(prediction)
        )
        
        # Send analysis to Kafka
        producer.send(ANALYSIS_TOPIC, analysis.dict())
        analysis_results.append(analysis.dict())
        
        # If anomaly detected, generate alert
        if anomaly_score < -0.5:  # Threshold for anomaly
            alert = AlertMessage(
                sensor_id=data['sensor_id'],
                location=data['location'],
                timestamp=datetime.now(),
                asbestos_level=data['asbestos_level'],
                severity="ANOMALY",
                message=f"Anomalous pattern detected in asbestos readings at {data['location']}. Investigation recommended."
            )
            producer.send(ALERT_TOPIC, alert.dict())
            alerts.append(alert.dict())

# API Routes
@app.on_event("startup")
async def startup_event():
    """Initialize background tasks on startup"""
    background_tasks = BackgroundTasks()
    await start_kafka_consumer(background_tasks)

@app.post("/sensor-reading/")
async def add_sensor_reading(sensor_data: SensorReading):
    """API endpoint to add a new sensor reading"""
    process_sensor_data(sensor_data)
    return {"status": "success", "message": "Sensor reading processed"}

@app.get("/readings/")
async def get_readings(location: Optional[str] = None, limit: int = 100):
    """Get recent sensor readings, optionally filtered by location"""
    if location:
        filtered_readings = [r for r in sensor_readings if r['location'] == location]
    else:
        filtered_readings = sensor_readings
    
    return {"readings": filtered_readings[-limit:]}

@app.get("/alerts/")
async def get_alerts(severity: Optional[str] = None, limit: int = 50):
    """Get recent alerts, optionally filtered by severity"""
    if severity:
        filtered_alerts = [a for a in alerts if a['severity'] == severity.upper()]
    else:
        filtered_alerts = alerts
    
    return {"alerts": filtered_alerts[-limit:]}

@app.get("/analysis/")
async def get_analysis(location: Optional[str] = None, limit: int = 20):
    """Get recent analysis results, optionally filtered by location"""
    if location:
        filtered_analysis = [a for a in analysis_results if a['location'] == location]
    else:
        filtered_analysis = analysis_results
    
    return {"analysis": filtered_analysis[-limit:]}

@app.get("/status/")
async def get_system_status():
    """Get overall system status"""
    locations = set(r['location'] for r in sensor_readings)
    status = {}
    
    for location in locations:
        loc_readings = [r for r in sensor_readings if r['location'] == location]
        if not loc_readings:
            continue
            
        latest = max(loc_readings, key=lambda r: r['timestamp'])
        
        if latest['asbestos_level'] >= DANGER_THRESHOLD:
            status_level = "DANGER"
        elif latest['asbestos_level'] >= WARNING_THRESHOLD:
            status_level = "WARNING"
        else:
            status_level = "SAFE"
            
        status[location] = {
            "status": status_level,
            "latest_reading": latest['asbestos_level'],
            "last_updated": latest['timestamp']
        }
    
    return {
        "system_status": "operational",
        "locations": status,
        "total_sensors": len(set(r['sensor_id'] for r in sensor_readings)),
        "total_readings": len(sensor_readings),
        "total_alerts": len(alerts)
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
