# api.py

import logging
import asyncio
from flask import Flask, jsonify

from sensors.sensor_manager import SensorManager
from core.engine import BioSignalEngine

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)

sensor_manager = SensorManager()
engine = BioSignalEngine(sensor_manager)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "system": "BioSignal Gate",
        "version": "1.0.1"
    })


@app.route("/run", methods=["POST"])
def run_cycle():
    try:
        result = asyncio.run(engine.run_cycle())

        return jsonify(result), 200

    except Exception as e:
        logging.error(f"API failure: {str(e)}")

        return jsonify({
            "status": "error",
            "message": "Execution failed"
        }), 500


if __name__ == "__main__":
    logging.info("Starting BioSignal Gate API...")
    app.run(host="0.0.0.0", port=5000, debug=False)