  
# core/engine.py

import asyncio
from datetime import datetime

from core.signal_processor import SignalProcessor
from core.bio_signal_gate import BioSignalGate
from core.executor import ActionExecutor


class BioSignalEngine:
    def __init__(self, sensor):
        """
        sensor: injected sensor (simulation or real)
        """
        self.sensor = sensor
        self.processor = SignalProcessor()
        self.gate = BioSignalGate()
        self.executor = ActionExecutor()

    async def run_cycle(self):
        """
        One full system cycle:
        Measure → Process → Decide → Execute
        """

        raw = await self.sensor.measure()

        features = self.processor.calculate_features(raw)

        decision = self.gate.evaluate(features)

        if decision["decision"] == "PROCEED":
            await self.executor.execute("log_data", {
                "timestamp": datetime.now().isoformat(),
                "raw": raw,
                "features": features,
                "decision": decision
            })
        else:
            await self.executor.execute("wait", {"duration": 1})

        return decision