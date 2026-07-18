import os
import pandas as pd
from datetime import datetime

HISTORY_DIR = "history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "history.csv")

os.makedirs(HISTORY_DIR, exist_ok=True)


def save_history(statement, prediction, confidence):
    """Save one assessment to history."""

    new_data = pd.DataFrame({
        "Date": [datetime.now().strftime("%d-%m-%Y %H:%M")],
        "Statement": [statement],
        "Prediction": [prediction],
        "Confidence": [round(float(confidence), 2)]
    })

    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)
        history = pd.concat([history, new_data], ignore_index=True)
    else:
        history = new_data

    history.to_csv(HISTORY_FILE, index=False)


def load_history():
    """Load assessment history."""

    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame(
            columns=[
                "Date",
                "Statement",
                "Prediction",
                "Confidence"
            ]
        )

    return pd.read_csv(HISTORY_FILE)


def clear_history():
    """Delete history."""

    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)


def total_assessments():
    return len(load_history())


def average_confidence():
    history = load_history()

    if history.empty:
        return 0

    return round(history["Confidence"].astype(float).mean(), 2)


def latest_assessment():
    history = load_history()

    if history.empty:
        return None

    return history.iloc[-1]