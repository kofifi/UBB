import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    f1_score,
)

from um.data import Dataset

MetricFn = Callable[[Any, Any], float]

DEFAULT_METRICS: dict[str, MetricFn] = {
    "accuracy": accuracy_score,
    "f1_macro": lambda y_true, y_pred: f1_score(y_true, y_pred, average="macro"),
}


@dataclass(frozen=True)
class EvaluationResult:
    metrics: dict[str, float]
    y_true: np.ndarray
    y_pred: np.ndarray
    target_names: list[str] | None = None


class Evaluator:
    def __init__(self, metrics: dict[str, MetricFn] | None = None) -> None:
        self.metrics = metrics or DEFAULT_METRICS

    def evaluate(self, model: Any, dataset: Dataset) -> EvaluationResult:
        y_pred = model.predict(dataset.X)
        scores = {name: float(fn(dataset.y, y_pred)) for name, fn in self.metrics.items()}
        return EvaluationResult(scores, np.asarray(dataset.y), y_pred, dataset.target_names)


class Reporter(Protocol):
    def report(self, result: EvaluationResult) -> None: ...


class ConsoleReporter:
    def report(self, result: EvaluationResult) -> None:
        print(classification_report(result.y_true, result.y_pred, target_names=result.target_names))
        print(result.metrics)


class JsonMetricsReporter:
    def __init__(self, path: Path) -> None:
        self.path = path

    def report(self, result: EvaluationResult) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(result.metrics, indent=2))


class ConfusionMatrixReporter:
    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def report(self, result: EvaluationResult) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        ConfusionMatrixDisplay.from_predictions(
            result.y_true, result.y_pred, display_labels=result.target_names
        )
        plt.savefig(self.directory / "confusion_matrix.png", bbox_inches="tight")
        plt.close()


def report_all(result: EvaluationResult, reporters: Sequence[Reporter]) -> None:
    for reporter in reporters:
        reporter.report(result)
