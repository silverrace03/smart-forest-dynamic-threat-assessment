from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class VirtualEvent:
    node_id: str
    zone_id: str
    event_type: str
    confidence: float
    severity: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if not 0 <= self.severity <= 100:
            raise ValueError("severity must be between 0 and 100")


@dataclass(frozen=True)
class ThreatAssessment:
    score: float
    category: str
    components: dict[str, float]
    adjustments: list[str]
    recommended_action: str

