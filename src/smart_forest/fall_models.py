from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Standardizer:
    mean_: np.ndarray | None = None
    scale_: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> "Standardizer":
        self.mean_ = x.mean(axis=0)
        self.scale_ = x.std(axis=0)
        self.scale_[self.scale_ == 0] = 1.0
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mean_) / self.scale_


class LogisticRegressionGD:
    def __init__(self, learning_rate=0.04, epochs=3500, l2=0.01):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.l2 = l2
        self.weights = None
        self.bias = 0.0

    def fit(self, x, y):
        self.weights = np.zeros(x.shape[1], dtype=float)
        for _ in range(self.epochs):
            scores = np.clip(x @ self.weights + self.bias, -30, 30)
            probabilities = 1 / (1 + np.exp(-scores))
            error = probabilities - y
            grad_w = x.T @ error / len(y) + self.l2 * self.weights
            grad_b = error.mean()
            self.weights -= self.learning_rate * grad_w
            self.bias -= self.learning_rate * grad_b
        return self

    def predict_score(self, x):
        scores = np.clip(x @ self.weights + self.bias, -30, 30)
        return 1 / (1 + np.exp(-scores))

    def predict(self, x):
        return (self.predict_score(x) >= 0.5).astype(int)


class LinearSVMGD:
    def __init__(self, learning_rate=0.01, epochs=3000, regularization=0.01):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.regularization = regularization
        self.weights = None
        self.bias = 0.0

    def fit(self, x, y):
        labels = np.where(y == 1, 1.0, -1.0)
        self.weights = np.zeros(x.shape[1], dtype=float)
        for epoch in range(self.epochs):
            margins = labels * (x @ self.weights + self.bias)
            active = margins < 1
            grad_w = self.regularization * self.weights
            grad_b = 0.0
            if np.any(active):
                grad_w -= (x[active].T @ labels[active]) / len(y)
                grad_b -= labels[active].sum() / len(y)
            rate = self.learning_rate / (1 + epoch * 0.0005)
            self.weights -= rate * grad_w
            self.bias -= rate * grad_b
        return self

    def predict_score(self, x):
        raw = x @ self.weights + self.bias
        return 1 / (1 + np.exp(-np.clip(raw, -30, 30)))

    def predict(self, x):
        return ((x @ self.weights + self.bias) >= 0).astype(int)


class RandomForestLite:
    """Compact bootstrapped forest for a transparent dependency-light baseline."""

    def __init__(self, n_estimators=80, max_depth=5, min_samples_leaf=5, seed=42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.seed = seed
        self.trees = []

    def fit(self, x, y):
        rng = np.random.default_rng(self.seed)
        self.trees = []
        for _ in range(self.n_estimators):
            indices = rng.integers(0, len(y), len(y))
            self.trees.append(self._grow(x[indices], y[indices], 0, rng))
        return self

    def _grow(self, x, y, depth, rng):
        probability = float(y.mean())
        if depth >= self.max_depth or len(y) < 2 * self.min_samples_leaf or probability in (0, 1):
            return {"probability": probability}

        feature_count = max(1, int(np.sqrt(x.shape[1])))
        features = rng.choice(x.shape[1], feature_count, replace=False)
        best = None
        parent_gini = 2 * probability * (1 - probability)

        for feature in features:
            candidates = np.unique(np.quantile(x[:, feature], np.linspace(0.1, 0.9, 9)))
            for threshold in candidates:
                left = x[:, feature] <= threshold
                left_n = int(left.sum())
                right_n = len(y) - left_n
                if left_n < self.min_samples_leaf or right_n < self.min_samples_leaf:
                    continue
                left_p, right_p = y[left].mean(), y[~left].mean()
                gini = (left_n * 2 * left_p * (1-left_p) + right_n * 2 * right_p * (1-right_p)) / len(y)
                gain = parent_gini - gini
                if best is None or gain > best[0]:
                    best = (gain, int(feature), float(threshold), left)

        if best is None or best[0] <= 1e-8:
            return {"probability": probability}
        _, feature, threshold, left = best
        return {
            "feature": feature,
            "threshold": threshold,
            "probability": probability,
            "left": self._grow(x[left], y[left], depth + 1, rng),
            "right": self._grow(x[~left], y[~left], depth + 1, rng),
        }

    def _tree_score(self, tree, row):
        while "feature" in tree:
            tree = tree["left"] if row[tree["feature"]] <= tree["threshold"] else tree["right"]
        return tree["probability"]

    def predict_score(self, x):
        return np.array([
            np.mean([self._tree_score(tree, row) for tree in self.trees])
            for row in x
        ])

    def predict(self, x):
        return (self.predict_score(x) >= 0.5).astype(int)


def binary_metrics(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    safe_div = lambda a, b: float(a / b) if b else 0.0
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    return {
        "accuracy": safe_div(tp + tn, len(y_true)),
        "precision": precision,
        "recall": recall,
        "f1": safe_div(2 * precision * recall, precision + recall),
        "specificity": safe_div(tn, tn + fp),
        "tn": tn, "fp": fp, "fn": fn, "tp": tp,
    }

