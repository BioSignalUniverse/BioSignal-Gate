
# core/bio_signal_gate.py

import json
import os


class BioSignalGate:
    def __init__(self, config_path="config/thresholds.json"):

        if os.path.exists(config_path):
            with open(config_path) as f:
                cfg = json.load(f)

            self.thresholds = cfg.get("thresholds", {})
            self.weights = cfg.get("weights", {})
            self.decision_threshold = cfg.get("decision_threshold", 0.7)

        else:
            # Safe defaults
            self.thresholds = {}
            self.weights = {}
            self.decision_threshold = 0.7

        self.total_weight = sum(self.weights.values()) if self.weights else 1.0

    def evaluate(self, features: dict):
        score = 0.0
        details = {}

        for feat, value in features.items():
            if feat in self.thresholds and feat in self.weights:
                threshold = self.thresholds[feat]
                weight = self.weights[feat]

                ratio = value / threshold if threshold != 0 else 0
                contribution = min(max(ratio, 0), 1) * weight

                score += contribution

                details[feat] = {
                    "value": round(value, 3),
                    "threshold": threshold,
                    "contribution": round(contribution, 3)
                }

        normalized_score = score / self.total_weight

        proceed = normalized_score >= self.decision_threshold

        return {
            "decision": "PROCEED" if proceed else "WAIT",
            "score": round(normalized_score, 3),
            "details": details
        }