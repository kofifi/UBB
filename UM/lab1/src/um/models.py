from collections.abc import Callable
from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

EstimatorBuilder = Callable[[dict[str, Any], int], BaseEstimator]


class ModelRegistry:
    def __init__(self) -> None:
        self._builders: dict[str, EstimatorBuilder] = {}

    def register(self, name: str) -> Callable[[EstimatorBuilder], EstimatorBuilder]:
        def decorator(builder: EstimatorBuilder) -> EstimatorBuilder:
            self._builders[name] = builder
            return builder

        return decorator

    def create(self, name: str, params: dict[str, Any], seed: int) -> BaseEstimator:
        if name not in self._builders:
            raise ValueError(f"Unknown model '{name}'. Available: {self.names}")
        return self._builders[name](params, seed)

    @property
    def names(self) -> list[str]:
        return sorted(self._builders)


registry = ModelRegistry()


@registry.register("random_forest")
def _random_forest(params: dict[str, Any], seed: int) -> BaseEstimator:
    return RandomForestClassifier(random_state=seed, **params)


@registry.register("logistic_regression")
def _logistic_regression(params: dict[str, Any], seed: int) -> BaseEstimator:
    return LogisticRegression(random_state=seed, **params)


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = X.select_dtypes(exclude="number").columns.tolist()
    numeric_pipe = Pipeline(
        [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    )
    categorical_pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        [("num", numeric_pipe, numeric), ("cat", categorical_pipe, categorical)]
    )


class PipelineFactory:
    def __init__(self, model_registry: ModelRegistry = registry) -> None:
        self.registry = model_registry

    def build(self, X: pd.DataFrame, name: str, params: dict[str, Any], seed: int) -> Pipeline:
        estimator = self.registry.create(name, params, seed)
        return Pipeline([("preprocess", build_preprocessor(X)), ("model", estimator)])
