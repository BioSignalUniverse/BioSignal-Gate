# api.py

from flask import Flask, request, jsonify
import asyncio

from sensors.sensor_manager import SensorManager
from core.engine import BioSignalEngine

app = Flask(__name__)

# Initialize system once
sensor_manager = SensorManager()
engine = BioSignalEngine(sensor_manager)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "system": "BioSignal Gate",
        "status": "running",
        "version": "1.0.0"
    })


@app.route("/run", methods=["POST"])
def run_cycle():
    """
    Runs one Measure → Process → Decide → Execute cycle.
    Optional: can accept external raw data in future.
    """

    result = asyncio.run(engine.run_cycle())

    return jsonify(result)


if __name__ == "__main__":
    print("BioSignal Gate API starting...")
    app.run(host="0.0.0.0", port=5000, debug=True)