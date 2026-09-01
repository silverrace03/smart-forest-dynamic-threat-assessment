import unittest

import numpy as np

from src.smart_forest.fall_models import LogisticRegressionGD, Standardizer, binary_metrics


class FallModelUtilityTests(unittest.TestCase):
    def test_binary_metrics_known_values(self):
        metrics = binary_metrics(np.array([0, 0, 1, 1]), np.array([0, 1, 1, 1]))
        self.assertEqual(metrics["tn"], 1)
        self.assertEqual(metrics["fp"], 1)
        self.assertEqual(metrics["fn"], 0)
        self.assertEqual(metrics["tp"], 2)
        self.assertAlmostEqual(metrics["recall"], 1.0)

    def test_logistic_model_learns_separable_data(self):
        x = np.array([[-2.0], [-1.0], [1.0], [2.0]])
        y = np.array([0, 0, 1, 1])
        scaler = Standardizer().fit(x)
        model = LogisticRegressionGD(epochs=1000).fit(scaler.transform(x), y)
        np.testing.assert_array_equal(model.predict(scaler.transform(x)), y)


if __name__ == "__main__":
    unittest.main()
