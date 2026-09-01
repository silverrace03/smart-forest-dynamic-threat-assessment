import json
from pathlib import Path

from .models import VirtualEvent
from .threat_engine import DynamicThreatEngine


def load_engine() -> DynamicThreatEngine:
    path = Path(__file__).parents[2] / "config" / "dti.json"
    with path.open(encoding="utf-8") as handle:
        return DynamicThreatEngine(json.load(handle))


def demo() -> None:
    engine = load_engine()
    scenarios = {
        "normal movement": [
            VirtualEvent("NODE-01", "general", "movement", 0.72, 25),
        ],
        "possible illegal logging": [
            VirtualEvent("NODE-02", "poaching_hotspot", "movement", 0.88, 45),
            VirtualEvent("NODE-02", "poaching_hotspot", "chainsaw", 0.93, 90),
        ],
        "ranger emergency": [
            VirtualEvent("RANGER-01", "ranger_patrol", "ranger_fall", 0.91, 85),
            VirtualEvent("RANGER-01", "ranger_patrol", "ranger_inactivity", 0.95, 90),
        ],
    }
    for name, events in scenarios.items():
        result = engine.assess(events, events[0].zone_id)
        print(f"{name}: DTI={result.score:.2f} {result.category}")
        print(f"  action: {result.recommended_action}")
        if result.adjustments:
            print(f"  adjustments: {', '.join(result.adjustments)}")


if __name__ == "__main__":
    demo()
