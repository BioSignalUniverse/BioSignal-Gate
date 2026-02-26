# api.py

import logging
import asyncio
from flask import Flask, request, jsonify

from sensors.sensor_manager import SensorManager
from core.engine import BioSignalEngine

# --------------------------------------------------
# Logging Setup
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("biosignal-gate")

# --------------------------------------------------
# App Initialization
# --------------------------------------------------

app = Flask(__name__)

sensor_manager = SensorManager()
engine = BioSignalEngine(sensor_manager)


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "system": "BioSignal Gate",
        "version": "1.0.1"
    })


# --------------------------------------------------
# Run One Cycle
# --------------------------------------------------

@app.route("/run", methods=["POST"])
def run_cycle():
    try:
        logger.info("Cycle requested")

        result = asyncio.run(engine.run_cycle())

        return jsonify({
            "status": "success",
            "result": result
        }), 200

    except Exception as e:
        logger.error(f"Cycle failed: {str(e)}")

        return jsonify({
            "status": "error",
            "message": "Execution failed"
        }), 500


# --------------------------------------------------
# Start Server
# --------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting BioSignal Gate API...")
    app.run(host="0.0.0.0", port=5000, debug=False)