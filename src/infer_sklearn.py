# src/infer_sklearn.py
import sys
import numpy as np
from PIL import Image
import joblib
import os

if len(sys.argv) < 2:
    print("Usage: python src/infer_sklearn.py path/to/image.jpg")
    sys.exit(1)

img_path = sys.argv[1]
model_file = "models/sklearn_logreg.joblib"
if not os.path.exists(model_file):
    print("Model not found. Train first (python src/train_sklearn.py).")
    sys.exit(1)

data = joblib.load(model_file)
clf = data["model"]
classes = data["classes"]

IMG_SIZE = (64, 64)
img = Image.open(img_path).convert("RGB").resize(IMG_SIZE)
arr = np.asarray(img).astype(np.float32) / 255.0
feat = arr.flatten().reshape(1, -1)
pred = clf.predict(feat)[0]
proba = clf.predict_proba(feat)[0] if hasattr(clf, "predict_proba") else None

print("Prediction:", pred)
if proba is not None:
    # print class probabilities nicely
    for cls, p in zip(clf.classes_, proba):
        print(f"{cls}: {p:.3f}")
