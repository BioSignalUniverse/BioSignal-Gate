
# sensors/polar_sensor.py

import asyncio
import os
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional

from bleak import BleakClient, BleakScanner
from sensors.base_sensor import BaseSensor

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"


class PolarH10Sensor(BaseSensor):

    def __init__(self):
        self.client: Optional[BleakClient] = None
        self.device = None
        self.connected = False

        self.heart_rate = 70.0
        self.rr_intervals: list[float] = []
        self.all_rr_buffer: list[float] = []
        self.signal_quality = 0.7
        self.last_update = None

    async def discover_and_connect(self) -> bool:

        devices = await BleakScanner.discover(timeout=5.0)

        for d in devices:
            if d.name and "Polar H10" in d.name:
                self.device = d
                break

        if not self.device:
            return False

        try:
            self.client = BleakClient(self.device.address)
            await self.client.connect()
            await self.client.start_notify(HR_UUID, self._hr_handler)

            self.connected = True
            return True

        except Exception:
            self.connected = False
            return False

    def _hr_handler(self, sender, data):

        try:
            bytes_data = bytes(data)

            if bytes_data[0] & 0x01:
                hr = int.from_bytes(bytes_data[1:3], "little")
            else:
                hr = bytes_data[1]

            self.heart_rate = float(hr)
            self.last_update = datetime.now()

        except Exception:
            self.signal_quality = 0.5

    async def measure(self) -> Dict[str, Any]:

        if not self.connected:
            return {
                "timestamp": datetime.now().isoformat(),
                "hrv_rmssd": 50.0,
                "hr_mean": 70.0,
                "resp_rate": 16.0,
                "signal_quality": 0.6,
                "sensor_status": "POLAR_NOT_CONNECTED",
                "measurement_id": os.urandom(8).hex(),
                "rr_intervals": [],
                "data_source": "SIMULATION_FALLBACK"
            }

        # Real measurement (simplified)
        return {
            "timestamp": datetime.now().isoformat(),
            "hrv_rmssd": 60.0,  # Placeholder until RR processing added
            "hr_mean": self.heart_rate,
            "resp_rate": 16.0,
            "signal_quality": self.signal_quality,
            "sensor_status": "POLAR_H10_ACTIVE",
            "measurement_id": os.urandom(8).hex(),
            "rr_intervals": [],
            "data_source": "POLAR_H10_REAL"
        }