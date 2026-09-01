import unittest

from src.smart_forest.models import VirtualEvent
from src.smart_forest.simulator import load_engine


class ThreatEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = load_engine()

    def test_normal_movement_is_not_critical(self):
        result = self.engine.assess(
            [VirtualEvent("N1", "general", "movement", 0.7, 20)], "general"
        )
        self.assertEqual(result.category, "Safe")

    def test_correlated_intrusion_adds_bonus(self):
        events = [
            VirtualEvent("N2", "poaching_hotspot", "movement", 0.9, 45),
            VirtualEvent("N2", "poaching_hotspot", "chainsaw", 0.95, 90),
        ]
        result = self.engine.assess(events, "poaching_hotspot")
        self.assertTrue(any("movement and chainsaw" in x for x in result.adjustments))
        self.assertGreater(result.score, 30)

    def test_fall_and_inactivity_has_critical_floor(self):
        events = [
            VirtualEvent("R1", "ranger_patrol", "ranger_fall", 0.9, 80),
            VirtualEvent("R1", "ranger_patrol", "ranger_inactivity", 0.9, 80),
        ]
        result = self.engine.assess(events, "ranger_patrol")
        self.assertGreaterEqual(result.score, 85)
        self.assertEqual(result.category, "Critical")

    def test_sos_is_critical(self):
        result = self.engine.assess(
            [VirtualEvent("R1", "general", "ranger_sos", 1.0, 100)], "general"
        )
        self.assertEqual(result.score, 100)
        self.assertEqual(result.category, "Critical")


if __name__ == "__main__":
    unittest.main()
