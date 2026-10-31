from um.config import Config, resolve
from um.data import CsvLoader, DataLoader, IrisLoader, StratifiedSplitter
from um.evaluation import (
    ConfusionMatrixReporter,
    ConsoleReporter,
    Evaluator,
    JsonMetricsReporter,
    Reporter,
)
from um.models import PipelineFactory
from um.repository import JoblibModelRepository
from um.training import Trainer


def build_loader(cfg: Config) -> DataLoader:
    if cfg.data.source == "iris":
        return IrisLoader()
    if cfg.data.source == "csv":
        if not cfg.data.path:
            raise ValueError("data.path is required when data.source is 'csv'")
        return CsvLoader(resolve(cfg.data.path), cfg.data.target)
    raise ValueError(f"Unknown data source '{cfg.data.source}'")


def build_splitter(cfg: Config) -> StratifiedSplitter:
    return StratifiedSplitter(cfg.data.test_size, cfg.seed)


def build_repository(cfg: Config) -> JoblibModelRepository:
    return JoblibModelRepository(cfg.paths.model)


def build_reporters(cfg: Config) -> list[Reporter]:
    return [
        ConsoleReporter(),
        JsonMetricsReporter(cfg.paths.metrics),
        ConfusionMatrixReporter(cfg.paths.figures),
    ]


def build_trainer(cfg: Config) -> Trainer:
    return Trainer(
        loader=build_loader(cfg),
        splitter=build_splitter(cfg),
        pipeline_factory=PipelineFactory(),
        repository=build_repository(cfg),
        evaluator=Evaluator(),
        reporters=build_reporters(cfg),
    )
