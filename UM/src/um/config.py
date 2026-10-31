from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "config.yaml"


def resolve(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else PROJECT_ROOT / p


@dataclass(frozen=True)
class DataConfig:
    source: str = "iris"
    path: str | None = None
    target: str = "target"
    test_size: float = 0.2


@dataclass(frozen=True)
class ModelConfig:
    name: str = "random_forest"
    params: dict[str, dict[str, Any]] = field(default_factory=dict)

    @property
    def selected_params(self) -> dict[str, Any]:
        return self.params.get(self.name) or {}


@dataclass(frozen=True)
class PathsConfig:
    model: Path = resolve("models/model.joblib")
    metrics: Path = resolve("reports/metrics.json")
    figures: Path = resolve("reports/figures")


@dataclass(frozen=True)
class Config:
    seed: int = 42
    data: DataConfig = field(default_factory=DataConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Config":
        return cls(
            seed=raw.get("seed", 42),
            data=DataConfig(**raw.get("data", {})),
            model=ModelConfig(**raw.get("model", {})),
            paths=PathsConfig(**{k: resolve(v) for k, v in raw.get("paths", {}).items()}),
        )

    @classmethod
    def from_yaml(cls, path: str | Path = DEFAULT_CONFIG) -> "Config":
        with open(path) as f:
            return cls.from_dict(yaml.safe_load(f) or {})
