from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import ThreatAssessment, VirtualEvent


EVENT_DOMAIN = {
    "background": "wildlife",
    "movement": "wildlife",
    "human_intrusion": "poaching",
    "gunshot": "poaching",
    "chainsaw": "poaching",
    "smoke": "environmental",
    "high_temperature": "environmental",
    "fire": "environmental",
    "ranger_fall": "ranger",
    "ranger_inactivity": "ranger",
    "ranger_sos": "ranger",
}


class DynamicThreatEngine:
    """Small, explainable DTI baseline suitable for thesis experiments."""

    def __init__(self, config: dict):
        self.weights = config["weights"]
        self.thresholds = config["thresholds"]
        self.bonuses = config["correlation_bonuses"]
        self.minimum_scores = config["minimum_scores"]
        self.zones = config["zones"]

    def assess(self, events: Iterable[VirtualEvent], zone_id: str) -> ThreatAssessment:
        events = list(events)
        domain_values: dict[str, list[float]] = defaultdict(list)
        event_types = {event.event_type for event in events}
        importance = self.zones.get(zone_id, {"importance": 1.0})["importance"]

        for event in events:
            domain = EVENT_DOMAIN.get(event.event_type)
            if domain:
                domain_values[domain].append(
                    min(100.0, event.severity * event.confidence * importance)
                )

        components = {
            domain: max(domain_values.get(domain, [0.0]))
            for domain in self.weights
        }
        score = sum(self.weights[d] * components[d] for d in self.weights)
        adjustments: list[str] = []

        score = self._add_bonus(
            score, event_types, {"movement", "chainsaw"},
            "movement_and_chainsaw", adjustments
        )
        score = self._add_bonus(
            score, event_types, {"movement", "gunshot"},
            "movement_and_gunshot", adjustments
        )
        score = self._add_bonus(
            score, event_types, {"smoke", "high_temperature"},
            "smoke_and_high_temperature", adjustments
        )

        if {"ranger_fall", "ranger_inactivity"}.issubset(event_types):
            score = max(score, self.minimum_scores["ranger_fall_with_inactivity"])
            adjustments.append("minimum 85: ranger fall followed by inactivity")
        if "ranger_sos" in event_types:
            score = max(score, self.minimum_scores["ranger_sos"])
            adjustments.append("critical override: ranger SOS")

        score = round(min(100.0, score), 2)
        category, action = self._category(score)
        return ThreatAssessment(score, category, components, adjustments, action)

    def _add_bonus(self, score, event_types, required, key, adjustments):
        if required.issubset(event_types):
            bonus = self.bonuses[key]
            adjustments.append(f"+{bonus}: {key.replace('_', ' ')}")
            return score + bonus
        return score

    def _category(self, score: float) -> tuple[str, str]:
        if score <= self.thresholds["safe_max"]:
            return "Safe", "Continue normal monitoring"
        if score <= self.thresholds["moderate_max"]:
            return "Moderate", "Increase virtual monitoring frequency"
        if score <= self.thresholds["high_max"]:
            return "High", "Notify control centre and review evidence"
        return "Critical", "Initiate immediate prioritized response"

