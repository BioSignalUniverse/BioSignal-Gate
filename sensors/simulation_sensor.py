
# sensors/simulation_sensor.py

import os
import numpy as np
from datetime import datetime
from typing import Dict, Any

from sensors.base_sensor import BaseSensor


class SimulationSensor(BaseSensor):

    async def measure(self) -> Dict[str, Any]:

        hrv = np.random.uniform(20, 120)
        hr = np.random.uniform(60, 100)
        resp = np.random.uniform(12, 20)

        return {
            "timestamp": datetime.now().isoformat(),
            "hrv_rmssd": float(hrv),
            "hr_mean": float(hr),
            "resp_rate": float(resp),
            "signal_quality": 0.9,
            "sensor_status": "SIMULATION",
            "measurement_id": os.urandom(8).hex(),
            "rr_intervals": []
        }