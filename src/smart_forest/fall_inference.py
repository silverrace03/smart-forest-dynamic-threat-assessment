from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

from .models import VirtualEvent


class FallDetector:
    def __init__(self, model_path: str | Path):
        with Path(model_path).open("rb") as handle:
            artifact = pickle.load(handle)
        self.name = artifact["name"]
        self.features = artifact["features"]
        self.uses_standardization = artifact["uses_standardization"]
        self.standardizer = artifact["standardizer"]
        self.model = artifact["model"]

    def predict(self, feature_values: dict[str, float]) -> tuple[int, float]:
        missing = [name for name in self.features if name not in feature_values]
        if missing:
            raise ValueError(f"missing fall-model features: {', '.join(missing)}")
        x = np.array([[feature_values[name] for name in self.features]], dtype=float)
        if self.uses_standardization:
            x = self.standardizer.transform(x)
        prediction = int(self.model.predict(x)[0])
        confidence = float(self.model.predict_score(x)[0])
        return prediction, confidence

    def to_virtual_event(self, feature_values, node_id, zone_id, inactivity=False):
        prediction, fall_probability = self.predict(feature_values)
        if prediction == 0:
            return VirtualEvent(node_id, zone_id, "background", 1-fall_probability, 5)
        return VirtualEvent(
            node_id,
            zone_id,
            "ranger_fall",
            fall_probability,
            85,
            metadata={"post_fall_inactivity": bool(inactivity), "model": self.name},
        )

