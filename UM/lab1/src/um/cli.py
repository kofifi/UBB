import argparse

import pandas as pd

from um import container
from um.config import DEFAULT_CONFIG, Config
from um.evaluation import Evaluator, report_all


def _parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="path to YAML config")
    return parser


def train() -> None:
    args = _parser("Train a model.").parse_args()
    cfg = Config.from_yaml(args.config)
    container.build_trainer(cfg).run(cfg.model.name, cfg.model.selected_params, cfg.seed)
    print(f"Model saved to {cfg.paths.model}")


def evaluate() -> None:
    args = _parser("Evaluate the saved model on the test split.").parse_args()
    cfg = Config.from_yaml(args.config)
    _, test = container.build_splitter(cfg).split(container.build_loader(cfg).load())
    model = container.build_repository(cfg).load()
    report_all(Evaluator().evaluate(model, test), container.build_reporters(cfg))


def predict() -> None:
    parser = _parser("Predict labels for rows of a CSV file.")
    parser.add_argument("input", help="CSV with the same feature columns as training data")
    parser.add_argument("-o", "--output", default="predictions.csv")
    args = parser.parse_args()
    cfg = Config.from_yaml(args.config)

    model = container.build_repository(cfg).load()
    df = pd.read_csv(args.input)
    df["prediction"] = model.predict(df)
    df.to_csv(args.output, index=False)
    print(f"Predictions saved to {args.output}")
