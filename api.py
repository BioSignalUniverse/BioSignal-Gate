# api.py

import asyncio
import logging
from flask import Flask, jsonify, render_template

from sensors.sensor_manager import SensorManager
from core.engine import BioSignalEngine

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

sensor_manager = SensorManager()
asyncio.run(sensor_manager.initialize())

engine = BioSignalEngine(sensor_manager)

# Store last result globally for dashboard
last_result = {
    "status": "waiting",
    "decision": "N/A",
    "score": 0.0,
    "sensor_status": "N/A",
    "timestamp": "N/A"
}

@app.route("/run", methods=["POST"])
def run_cycle():
    global last_result

    result = asyncio.run(engine.run_cycle())

    if result.get("status") == "success":
        last_result = {
            "status": "running",
            "decision": result["decision"]["decision"],
            "score": result["decision"]["score"],
            "sensor_status": result["raw"]["sensor_status"],
            "timestamp": result["timestamp"]
        }

    return jsonify(result)

@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        status=last_result["status"],
        decision=last_result["decision"],
        score=last_result["score"],
        sensor_status=last_result["sensor_status"],
        timestamp=last_result["timestamp"]
    )

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
