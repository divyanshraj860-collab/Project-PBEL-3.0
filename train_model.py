import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

# -------------------------
# Load Data
# -------------------------

df = pd.read_csv("data/Combined Data.csv")

if "Unnamed: 0" in df.columns:
    df.drop(columns=["Unnamed: 0"], inplace=True)

df = df.dropna(subset=["statement", "status"])

df["statement"] = df["statement"].astype(str)

X = df["statement"]
y = df["status"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# -------------------------
# Models
# -------------------------

models = {

    "Logistic Regression": Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000))
    ]),

    "Random Forest": Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ))
    ]),

    "Linear SVM": Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf",
            CalibratedClassifierCV(
                LinearSVC(),
                cv=5
            )
        )
    ])
}

best_model = None
best_accuracy = 0

print("=" * 50)

for name, model in models.items():

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)

    print(f"{name}: {acc*100:.2f}%")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model

print("=" * 50)
print(f"Best Accuracy: {best_accuracy*100:.2f}%")

joblib.dump(best_model, "models/model.pkl")

print("Best model saved successfully!")