
# sensors/sensor_manager.py

from sensors.simulation_sensor import SimulationSensor


class SensorManager:

    def __init__(self):
        self.sensor = SimulationSensor()

    async def initialize(self):
        """
        Later we can attempt real device connection here.
        For now, simulation is the default.
        """
        pass

    async def measure(self):
        return await self.sensor.measure()