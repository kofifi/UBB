from collections.abc import Sequence
from typing import Any

from um.data import DataLoader, DataSplitter
from um.evaluation import EvaluationResult, Evaluator, Reporter, report_all
from um.models import PipelineFactory
from um.repository import ModelRepository


class Trainer:
    def __init__(
        self,
        loader: DataLoader,
        splitter: DataSplitter,
        pipeline_factory: PipelineFactory,
        repository: ModelRepository,
        evaluator: Evaluator,
        reporters: Sequence[Reporter] = (),
    ) -> None:
        self.loader = loader
        self.splitter = splitter
        self.pipeline_factory = pipeline_factory
        self.repository = repository
        self.evaluator = evaluator
        self.reporters = reporters

    def run(self, model_name: str, params: dict[str, Any], seed: int) -> EvaluationResult:
        train, test = self.splitter.split(self.loader.load())
        model = self.pipeline_factory.build(train.X, model_name, params, seed)
        model.fit(train.X, train.y)
        self.repository.save(model)

        result = self.evaluator.evaluate(model, test)
        report_all(result, self.reporters)
        return result
