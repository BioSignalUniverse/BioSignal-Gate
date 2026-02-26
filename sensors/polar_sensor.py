# sensors/polar_sensor.py

import asyncio
import os
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, List

from bleak import BleakClient, BleakScanner
from sensors.base_sensor import BaseSensor


HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"


class PolarH10Sensor(BaseSensor):

    def __init__(self):
        self.client: Optional[BleakClient] = None
        self.device = None
        self.connected = False

        self.heart_rate = 70.0
        self.rr_buffer: List[float] = []
        self.max_buffer_size = 300

        self.signal_quality = 0.7
        self.last_update = None

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------

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

    # --------------------------------------------------
    # HR Notification Handler
    # --------------------------------------------------

    def _hr_handler(self, sender, data):

        try:
            bytes_data = bytes(data)
            flags = bytes_data[0]

            # Heart rate parsing
            if flags & 0x01:
                hr = int.from_bytes(bytes_data[1:3], "little")
            else:
                hr = bytes_data[1]

            self.heart_rate = float(hr)

            # RR intervals parsing
            if flags & 0x10:
                offset = 3 if flags & 0x01 else 2

                while offset + 2 <= len(bytes_data):
                    rr_raw = int.from_bytes(
                        bytes_data[offset:offset+2],
                        "little"
                    )

                    rr_ms = rr_raw / 1024.0 * 1000.0
                    self.rr_buffer.append(rr_ms)

                    offset += 2

                # Limit buffer size
                if len(self.rr_buffer) > self.max_buffer_size:
                    self.rr_buffer = self.rr_buffer[-self.max_buffer_size:]

            self.signal_quality = 1.0 if len(self.rr_buffer) >= 5 else 0.7
            self.last_update = datetime.now()

        except Exception:
            self.signal_quality = 0.5

    # --------------------------------------------------
    # True RMSSD Calculation
    # --------------------------------------------------

    def _calculate_rmssd(self) -> float:

        if len(self.rr_buffer) < 2:
            return 50.0  # Safe fallback

        rr = np.array(self.rr_buffer[-30:])
        diffs = np.diff(rr)

        return float(np.sqrt(np.mean(diffs ** 2)))

    # --------------------------------------------------
    # Measurement Interface
    # --------------------------------------------------

    async def measure(self) -> Dict[str, Any]:

        # If connected and recent data exists
        if (
            self.connected and
            self.last_update and
            (datetime.now() - self.last_update).seconds < 5
        ):

            hrv_rmssd = self._calculate_rmssd()

            return {
                "timestamp": datetime.now().isoformat(),
                "hrv_rmssd": hrv_rmssd,
                "hr_mean": self.heart_rate,
                "resp_rate": 16.0,
                "signal_quality": self.signal_quality,
                "sensor_status": "POLAR_H10_ACTIVE",
                "measurement_id": os.urandom(8).hex(),
                "rr_intervals": self.rr_buffer[-10:],
                "data_source": "POLAR_H10_REAL"
            }

        # Fallback to safe simulation
        return {
            "timestamp": datetime.now().isoformat(),
            "hrv_rmssd": 50.0,
            "hr_mean": 70.0,
            "resp_rate": 16.0,
            "signal_quality": 0.6,
            "sensor_status": "SIMULATION_FALLBACK",
            "measurement_id": os.urandom(8).hex(),
            "rr_intervals": [],
            "data_source": "SIMULATION"
        }

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    async def cleanup(self):

        if self.client and self.client.is_connected:
            await self.client.stop_notify(HR_UUID)
            await self.client.disconnect()