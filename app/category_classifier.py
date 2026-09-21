class CategoryClassifier:
    
    def __init__(self):
        self.model = None
        self.vectorizer = None

    def load_model(self, model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer

    def predict(self, text: str):
        # No trained model yet
        if self.model is None or self.vectorizer is None:
            return None

        text_vector = self.vectorizer.transform([text])

        prediction = self.model.predict(text_vector)[0]

        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(text_vector)[0]
            confidence = float(max(probabilities))
        else:
            confidence = 1.0

        return prediction, confidence