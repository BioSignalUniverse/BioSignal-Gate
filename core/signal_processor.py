
# core/signal_processor.py

import numpy as np
from typing import Dict


class SignalProcessor:

    @staticmethod
    def calculate_features(raw: Dict) -> Dict[str, float]:

        hrv = raw.get("hrv_rmssd", 0)
        hr = raw.get("hr_mean", 0)
        resp = raw.get("resp_rate", 0)

        features = {
            "hrv_log": np.log(hrv + 1),
            "normalized_hrv": (hrv - 20) / 100,
            "variability_index": hrv / hr if hr > 0 else 0,
            "resp_sync": 1 / (1 + np.exp(-(resp - 16))),
        }

        return features