# core/engine.py

import logging

from core.signal_processor import SignalProcessor
from core.bio_signal_gate import BioSignalGate
from core.executor import ActionExecutor


class BioSignalEngine:

    def __init__(self, sensor):
        self.sensor = sensor
        self.processor = SignalProcessor()
        self.gate = BioSignalGate()
        self.executor = ActionExecutor()

        self.logger = logging.getLogger("biosignal-gate.engine")

    async def run_cycle(self):

        try:
            raw = await self.sensor.measure()

            features = self.processor.calculate_features(raw)

            decision = self.gate.evaluate(features)

            await self.executor.execute("log_data", {
                "raw": raw,
                "features": features,
                "decision": decision
            })

            self.logger.info(f"Cycle completed: {decision['decision']}")

            return {
                "status": "success",
                "raw": raw,
                "features": features,
                "decision": decision
            }

        except Exception as e:
            self.logger.error(f"Engine error: {str(e)}")

            return {
                "status": "error",
                "message": "Engine execution failed"
            }