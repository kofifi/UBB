import pytest

from um.config import Config, PathsConfig


@pytest.fixture
def cfg(tmp_path) -> Config:
    return Config(
        paths=PathsConfig(
            model=tmp_path / "model.joblib",
            metrics=tmp_path / "metrics.json",
            figures=tmp_path / "figures",
        )
    )
