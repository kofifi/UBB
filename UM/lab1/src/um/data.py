from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class Dataset:
    X: pd.DataFrame
    y: pd.Series
    target_names: list[str] | None = None

    def __len__(self) -> int:
        return len(self.X)


class DataLoader(Protocol):
    def load(self) -> Dataset: ...


class IrisLoader:
    def load(self) -> Dataset:
        bunch = load_iris(as_frame=True)
        return Dataset(X=bunch.data, y=bunch.target, target_names=list(bunch.target_names))


class CsvLoader:
    def __init__(self, path: str | Path, target: str) -> None:
        self.path = Path(path)
        self.target = target

    def load(self) -> Dataset:
        df = pd.read_csv(self.path)
        return Dataset(X=df.drop(columns=[self.target]), y=df[self.target])


class DataSplitter(Protocol):
    def split(self, dataset: Dataset) -> tuple[Dataset, Dataset]: ...


class StratifiedSplitter:
    def __init__(self, test_size: float, seed: int) -> None:
        self.test_size = test_size
        self.seed = seed

    def split(self, dataset: Dataset) -> tuple[Dataset, Dataset]:
        X_train, X_test, y_train, y_test = train_test_split(
            dataset.X,
            dataset.y,
            test_size=self.test_size,
            random_state=self.seed,
            stratify=dataset.y,
        )
        names = dataset.target_names
        return Dataset(X_train, y_train, names), Dataset(X_test, y_test, names)
