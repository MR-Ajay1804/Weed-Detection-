from pathlib import Path

from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_PATH = BASE_DIR / "models" / "sklearn_logreg.joblib"
IMG_SIZE = (64, 64)
LABELS = ["weed", "crop"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def load_images(folder):
    X, y = [], []

    for label in LABELS:
        path = folder / label
        if not path.exists():
            raise SystemExit(f"Missing data folder: {path}")

        for img_path in path.iterdir():
            if img_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            try:
                img = Image.open(img_path).convert("RGB").resize(IMG_SIZE)
                arr = np.array(img).astype(np.float32) / 255.0

                X.append(arr.flatten())
                y.append(label)

                flip = np.fliplr(arr)
                X.append(flip.flatten())
                y.append(label)
            except Exception as exc:
                print("Error loading:", img_path, exc)

    return np.array(X), np.array(y)


print("Loading dataset...")
X, y = load_images(DATA_DIR)

print("Total samples:", len(X))

if len(X) == 0:
    raise SystemExit("No images found in data folder")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print("Train samples:", X_train.shape)
print("Test samples:", X_test.shape)
print("Training model...")

clf = LogisticRegression(
    max_iter=3000,
    solver="saga",
    random_state=42,
    n_jobs=-1,
)

clf.fit(X_train, y_train)

print("\nEvaluating model...\n")
y_pred = clf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

MODEL_PATH.parent.mkdir(exist_ok=True)

joblib.dump({
    "model": clf,
    "classes": np.unique(y_train),
}, MODEL_PATH)

print("\nModel saved at:", MODEL_PATH)
