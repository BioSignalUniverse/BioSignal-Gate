# core/engine.py

import logging
from datetime import datetime

from core.signal_processor import SignalProcessor
from core.bio_signal_gate import BioSignalGate
from core.executor import ActionExecutor


class BioSignalEngine:

    def __init__(self, sensor):
        """
        Sensor is injected (simulation or real).
        Engine does NOT know which one it is.
        """

        self.sensor = sensor
        self.processor = SignalProcessor()
        self.gate = BioSignalGate()
        self.executor = ActionExecutor()

        self.logger = logging.getLogger("biosignal-gate.engine")

    async def run_cycle(self):
        """
        Measure → Process → Decide → Execute
        Fully isolated, safe cycle.
        """

        try:
            # 1. MEASURE
            raw = await self.sensor.measure()

            # 2. PROCESS
            features = self.processor.calculate_features(raw)

            # 3. DECIDE
            decision = self.gate.evaluate(features)

            # 4. EXECUTE
            await self.executor.execute("log_data", {
                "timestamp": datetime.now().isoformat(),
                "raw": raw,
                "features": features,
                "decision": decision
            })

            self.logger.info(
                f"Cycle completed. Decision: {decision['decision']}"
            )

            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "raw": raw,
                "features": features,
                "decision": decision
            }

        except Exception as e:

            self.logger.error(f"Engine failure: {str(e)}")

            return {
                "status": "error",
                "message": "Engine execution failed"
            }