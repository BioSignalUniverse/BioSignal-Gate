# api.py

import asyncio
import logging
from flask import Flask, jsonify

from sensors.sensor_manager import SensorManager
from core.engine import BioSignalEngine

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("biosignal-gate")

# --------------------------------------------------
# App Setup
# --------------------------------------------------

app = Flask(__name__)

# Initialize system
sensor_manager = SensorManager()

# Attempt device connection once at startup
asyncio.run(sensor_manager.initialize())

engine = BioSignalEngine(sensor_manager)

# --------------------------------------------------
# Routes
# --------------------------------------------------

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
        logger.error(f"API error: {str(e)}")
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