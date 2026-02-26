
# sensors/base_sensor.py

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseSensor(ABC):
    """
    Abstract sensor interface.
    All sensors must implement `measure()`.
    """

    @abstractmethod
    async def measure(self) -> Dict[str, Any]:
        pass