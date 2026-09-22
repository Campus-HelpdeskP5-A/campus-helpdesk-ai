from pathlib import Path
import joblib


BASE_DIR = Path(__file__).resolve().parent.parent


class ModelRegistry:

    def __init__(self):
        self.models = {}

    def load_category_model(self):
        model_path = BASE_DIR / "models" / "category" / "category_model.joblib"
        vectorizer_path = BASE_DIR / "models" / "category" / "category_vectorizer.joblib"

        if not model_path.exists() or not vectorizer_path.exists():
            return None, None

        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

        self.models["category"] = model

        return model, vectorizer

    def load_sla_model(self):
        model_path = BASE_DIR / "models" / "sla" / "sla_model.joblib"

        if not model_path.exists():
            return None

        model = joblib.load(model_path)

        self.models["sla"] = model

        return model