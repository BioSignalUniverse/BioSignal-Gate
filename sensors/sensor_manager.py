# sensors/sensor_manager.py

from sensors.simulation_sensor import SimulationSensor
from sensors.polar_sensor import PolarH10Sensor


class SensorManager:

    def __init__(self):
        self.sensor = SimulationSensor()

    async def initialize(self):
        """
        Try to connect to Polar.
        If it fails, stay in simulation mode.
        """

        polar = PolarH10Sensor()
        connected = await polar.discover_and_connect()

        if connected:
            self.sensor = polar