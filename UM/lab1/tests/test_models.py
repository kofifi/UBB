import pytest

from um.data import IrisLoader
from um.models import ModelRegistry, PipelineFactory, registry


def test_registry_has_default_models():
    assert {"random_forest", "logistic_regression"} <= set(registry.names)


def test_registry_rejects_unknown_model():
    with pytest.raises(ValueError):
        ModelRegistry().create("nope", {}, 0)


def test_custom_model_can_be_registered():
    from sklearn.dummy import DummyClassifier

    reg = ModelRegistry()
    reg.register("dummy")(lambda params, seed: DummyClassifier(**params))
    ds = IrisLoader().load()
    model = PipelineFactory(reg).build(ds.X, "dummy", {}, 0).fit(ds.X, ds.y)
    assert len(model.predict(ds.X)) == len(ds)
