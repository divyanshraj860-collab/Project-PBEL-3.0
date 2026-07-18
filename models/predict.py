import os
import joblib
import numpy as np

MODEL_PATH = os.path.join("models", "model.pkl")

model = joblib.load(MODEL_PATH)


def predict_mental_health(text):
    prediction = model.predict([text])[0]

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([text])[0]
        classes = list(model.classes_)
        probabilities = np.round(probs * 100, 2).tolist()
        confidence = max(probabilities)
    else:
        classes = [prediction]
        probabilities = [100.0]
        confidence = 100.0

    return prediction, confidence, classes, probabilities


predict = predict_mental_health