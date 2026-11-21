import pandas as pd

from um.data import CsvLoader, IrisLoader, StratifiedSplitter


def test_iris_loader():
    ds = IrisLoader().load()
    assert ds.X.shape == (150, 4)
    assert ds.target_names == ["setosa", "versicolor", "virginica"]


def test_csv_loader(tmp_path):
    path = tmp_path / "data.csv"
    pd.DataFrame({"a": [1, 2], "b": ["x", "y"], "label": [0, 1]}).to_csv(path, index=False)
    ds = CsvLoader(path, "label").load()
    assert list(ds.X.columns) == ["a", "b"]
    assert ds.y.tolist() == [0, 1]


def test_stratified_splitter_keeps_class_balance():
    train, test = StratifiedSplitter(test_size=0.2, seed=0).split(IrisLoader().load())
    assert len(train) == 120 and len(test) == 30
    assert test.y.value_counts().nunique() == 1
