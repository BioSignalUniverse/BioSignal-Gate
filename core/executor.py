
# core/executor.py

import asyncio
import json
import os


class ActionExecutor:

    async def execute(self, action_type, data=None):

        if action_type == "log_data":
            filename = "session_log.jsonl"

            with open(filename, "a") as f:
                f.write(json.dumps(data) + "\n")

        elif action_type == "wait":
            await asyncio.sleep(data.get("duration", 1))

        else:
            pass