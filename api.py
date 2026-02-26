# api.py

from flask import Flask, request, jsonify
import asyncio

from sensors.sensor_manager import SensorManager
from core.engine import BioSignalEngine

app = Flask(__name__)

sensor_manager = SensorManager()
engine = BioSignalEngine(sensor_manager)


@app.route("/run", methods=["POST"])
def run_cycle():

    result = asyncio.run(engine.run_cycle())

    return jsonify(result)


@app.route("/status", methods=["GET"])
def status():

    return jsonify({
        "status": "running",
        "system": "BioSignal Gate",
        "version": "1.0"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)