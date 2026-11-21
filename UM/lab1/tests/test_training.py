import json

from um.config import Config
from um.container import build_trainer


def test_train_end_to_end(cfg: Config):
    result = build_trainer(cfg).run(cfg.model.name, {"n_estimators": 50}, cfg.seed)
    assert result.metrics["accuracy"] > 0.8
    assert cfg.paths.model.exists()
    assert json.loads(cfg.paths.metrics.read_text())["accuracy"] == result.metrics["accuracy"]
    assert (cfg.paths.figures / "confusion_matrix.png").exists()


def test_config_from_yaml_selects_params():
    cfg = Config.from_yaml()
    assert cfg.model.selected_params == cfg.model.params[cfg.model.name]
