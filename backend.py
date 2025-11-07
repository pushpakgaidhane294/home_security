import numpy as np
from datetime import datetime, timedelta

# Simulate devices
def get_devices():
    np.random.seed()  # for randomness in updates
    return [
        {"id": 1, "name": "Front Door Camera", "type": "camera", "status": np.random.choice(["active", "inactive"], p=[.8, .2]), "location": "Front Entrance", "battery": np.random.randint(70, 100)},
        {"id": 2, "name": "Motion Sensor - Living Room", "type": "sensor", "status": "active", "location": "Living Room", "battery": np.random.randint(80, 100)},
        {"id": 3, "name": "Smart Lock - Main Door", "type": "lock", "status": "active", "location": "Main Door", "battery": np.random.randint(50, 90)},
        {"id": 4, "name": "Window Sensor - Bedroom", "type": "sensor", "status": np.random.choice(["active", "inactive"], p=[.7, .3]), "location": "Bedroom", "battery": np.random.randint(30, 60)},
        {"id": 5, "name": "Garage Camera", "type": "camera", "status": "active", "location": "Garage", "battery": np.random.randint(90, 100)},
        {"id": 6, "name": "Back Door Sensor", "type": "sensor", "status": "active", "location": "Back Door", "battery": np.random.randint(60, 79)},
    ]

# Simulate alerts
def get_alerts():
    now = datetime.now()
    return [
        {"id": 1, "type": "warning", "message": "Motion detected at Front Entrance", "timestamp": now - timedelta(minutes=5), "severity": "medium"},
        {"id": 2, "type": "critical", "message": "Unauthorized access attempt at Main Door", "timestamp": now - timedelta(minutes=15), "severity": "high"},
        {"id": 3, "type": "info", "message": "Battery low on Window Sensor - Bedroom", "timestamp": now - timedelta(hours=1), "severity": "low"},
    ]

# Simulate activity log
def get_activity_log():
    np.random.seed()
    events = []
    now = datetime.now()
    for i in range(20):
        events.append({
            "timestamp": now - timedelta(minutes=i*10),
            "device": np.random.choice(["Front Door Camera", "Motion Sensor", "Smart Lock"]),
            "event": np.random.choice(["Motion Detected", "Door Opened", "Access Granted", "Battery Warning"]),
            "status": np.random.choice(["success", "warning", "error"])
        })
    return events
