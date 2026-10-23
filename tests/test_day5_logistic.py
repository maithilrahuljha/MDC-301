import numpy as np
from sklearn.pipeline import Pipeline

from week1.day5_logistic import demo_data, evaluate_binary, fit_logistic_demo


def _fitted():
    model, split = fit_logistic_demo()
    x_train, x_test, y_train, y_test = split
    return model, x_train, x_test, y_train, y_test


def test_fit_returns_scaled_logistic_pipeline_and_stratified_split():
    model, x_train, x_test, y_train, y_test = _fitted()
    assert isinstance(model, Pipeline)
    assert [name for name, _ in model.steps] == ["standardscaler", "logisticregression"]
    assert len(x_train) == 8 and len(x_test) == 4
    assert int(y_train.sum()) == 2 and int(y_test.sum()) == 1
    assert set(np.unique(np.concatenate([y_train, y_test]))) == {0, 1}


def test_positive_class_probabilities_are_valid_and_aligned():
    model, _, x_test, _, y_test = _fitted()
    report = evaluate_binary(model, x_test, y_test)
    probs = report["probabilities"]
    assert probs.shape == y_test.shape
    assert np.all((probs >= 0) & (probs <= 1))
    assert np.allclose(model.predict_proba(x_test).sum(axis=1), 1.0)


def test_confusion_matrix_uses_fixed_zero_one_order():
    model, _, x_test, _, y_test = _fitted()
    report = evaluate_binary(model, x_test, y_test)
    matrix = report["confusion_matrix"]
    assert matrix.shape == (2, 2)
    assert int(matrix.sum()) == len(y_test)
    assert int(matrix[1, :].sum()) == int(y_test.sum())
    assert int(matrix[:, 1].sum()) == int(report["predictions"].sum())


def test_precision_and_recall_are_from_confusion_counts():
    model, _, x_test, _, y_test = _fitted()
    report = evaluate_binary(model, x_test, y_test)
    tn, fp, fn, tp = report["confusion_matrix"].ravel()
    expected_precision = tp / (tp + fp) if tp + fp else 0.0
    expected_recall = tp / (tp + fn) if tp + fn else 0.0
    assert np.isclose(report["precision"], expected_precision)
    assert np.isclose(report["recall"], expected_recall)
