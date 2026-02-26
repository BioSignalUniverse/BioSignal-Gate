# core/executor.py

import os
import json
import asyncio
from typing import Dict, Any


class BioSignalEngine:
    """
    Core engine for executing actions on biosignal data.
    Includes Veto/Gate mechanism and data logging.
    """

    def __init__(self, lock_filename: str = "BIOGATE_ACTIVE.lock", log_filename: str = "session_log.jsonl"):
        self.lock_file = lock_filename
        self.log_file = log_filename

    # --------------------------------------------------
    # Action Executor
    # --------------------------------------------------

    async def execute(self, action_type: str, data: Dict[str, Any] = None):
        """
        Execute a specific action.
        Supported actions:
          - gate_arm / gate_release
          - write_data
          - wait
        """
        if action_type == "gate_arm":
            self._arm_gate()
        elif action_type == "gate_release":
            self._release_gate()
        elif action_type == "write_data" and data is not None:
            self._log_data(data)
        elif action_type == "wait" and data is not None:
            duration = data.get("duration", 1)
            await asyncio.sleep(duration)

    # --------------------------------------------------
    # Gate Mechanism