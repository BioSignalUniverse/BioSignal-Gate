# core/bio_signal_gate.py

import json
import os
from typing import Dict, Any


class BioSignalGate:
    """
    Config-driven decision gate.
    Evaluates physiological features using weighted thresholds.
    """

    def __init__(self, config_path: str = "config/thresholds.json"):

        if os.path.exists(config_path):
            with open(config_path) as f:
                cfg = json.load(f)

            self.thresholds = cfg.get("thresholds", {})
            self.weights = cfg.get("weights", {})
            self.decision_threshold = cfg.get("decision_threshold", 0.7)

        else:
            # Safe fallback defaults
            self.thresholds = {}
            self.weights = {}
            self.decision_threshold = 0.7

        self.total_weight = sum(self.weights.values()) if self.weights else 1.0

    # --------------------------------------------------
    # Evaluation Logic
    # --------------------------------------------------

    def evaluate(self, features: Dict[str, float]) -> Dict[str, Any]:

        score = 0.0
        details = {}

        for feature, value in features.items():

            if feature in self.thresholds and feature in self.weights:

                threshold = self.thresholds[feature]
                weight = self.weights[feature]

                # Normalize contribution (0–1 range)
                if threshold > 0:
                    ratio = value / threshold
                else:
                    ratio = 0

                contribution = min(max(ratio, 0), 1) * weight
                score += contribution

                details[feature] = {
                    "value": round(value, 3),
                    "threshold": threshold,
                    "contribution": round(contribution, 3)
                }

        normalized_score = (
            score / self.total_weight
            if self.total_weight > 0
            else 0
        )

        proceed = normalized_score >= self.decision_threshold

        return {
            "decision": "PROCEED" if proceed else "WAIT",
            "score": round(normalized_score, 3),
            "threshold_required": self.decision_threshold,
            "details": details
        }