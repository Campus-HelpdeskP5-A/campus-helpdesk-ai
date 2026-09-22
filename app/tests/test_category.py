from app.category_classifier import CategoryClassifier


def test_classifier_returns_none_without_model():
    classifier = CategoryClassifier()
    result = classifier.predict("AC is not working in room 101")

    assert result is None


def test_classifier_predicts_after_loading_model():
    import joblib
    from pathlib import Path

    model_dir = Path(__file__).resolve().parent.parent.parent / "models" / "category"
    model_path = model_dir / "category_model.joblib"
    vectorizer_path = model_dir / "category_vectorizer.joblib"

    if not model_path.exists() or not vectorizer_path.exists():
        # Lw el model mesh mawgood (lisa ma3molsh train), ne-skip
        import pytest
        pytest.skip("Trained category model not found. Run train_category_model.py first.")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    classifier = CategoryClassifier()
    classifier.load_model(model, vectorizer)

    result = classifier.predict("AC problem in the lab, thermostat not working")

    assert result is not None
    category, confidence = result
    assert isinstance(category, str)
    assert 0 <= confidence <= 1