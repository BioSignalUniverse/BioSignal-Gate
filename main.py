
from sensors.sensor_manager import SensorManager
from core.engine import BioSignalEngine

import asyncio

async def main():

    sensor_manager = SensorManager()
    await sensor_manager.initialize()

    engine = BioSignalEngine(sensor_manager)

    result = await engine.run_cycle()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())