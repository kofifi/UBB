from pathlib import Path
from typing import Any, Protocol

import joblib


class ModelRepository(Protocol):
    def save(self, model: Any) -> None: ...

    def load(self) -> Any: ...


class JoblibModelRepository:
    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, model: Any) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, self.path)

    def load(self) -> Any:
        return joblib.load(self.path)
