from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
IMG_SIZE = (64, 64)
MODEL_PATH = BASE_DIR / "models" / "sklearn_logreg.joblib"
MAX_UPLOAD_SIZE_MB = 5

UPLOAD_FOLDER.mkdir(exist_ok=True)


def cleanup_uploads(folder=UPLOAD_FOLDER, minutes=60):
    cutoff = datetime.now() - timedelta(minutes=minutes)
    for path in folder.iterdir():
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            if mtime < cutoff:
                path.unlink()


if not MODEL_PATH.exists():
    raise SystemExit(f"Model file not found: {MODEL_PATH}")

data = joblib.load(MODEL_PATH)
clf = data["model"]
classes = list(data["classes"])

app = Flask(__name__, static_folder=str(UPLOAD_FOLDER))
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE_MB * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def build_upload_name(filename):
    safe_name = secure_filename(filename)
    suffix = Path(safe_name).suffix.lower()
    stem = Path(safe_name).stem[:40] or "image"
    return f"{stem}-{uuid4().hex[:10]}{suffix}"


def predict_image(path):
    img = Image.open(path).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img).astype(np.float32) / 255.0
    feat = arr.flatten().reshape(1, -1)

    pred = clf.predict(feat)[0]
    if hasattr(clf, "predict_proba"):
        proba = clf.predict_proba(feat)[0]
        probs = {cls: float(p) for cls, p in zip(classes, proba)}
    else:
        probs = None

    return pred, probs


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file uploaded")

        file = request.files["file"]

        if file.filename == "":
            return render_template("index.html", error="No file selected")

        if file and allowed_file(file.filename):
            filename = build_upload_name(file.filename)
            path = Path(app.config["UPLOAD_FOLDER"]) / filename
            file.save(path)
            cleanup_uploads()

            try:
                pred, probs = predict_image(path)
            except Exception:
                path.unlink(missing_ok=True)
                return render_template("index.html", error="Please upload a valid plant image.")

            print("Prediction:", pred)
            return render_template(
                "index.html",
                result=pred,
                probs=probs,
                image_file=filename,
            )

        return render_template("index.html", error="Invalid file type")

    return render_template("index.html")


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error=f"File is too large. Please upload an image under {MAX_UPLOAD_SIZE_MB} MB.",
    ), 413


if __name__ == "__main__":
    print("Starting Weed Detection app...")
    app.run(debug=True)
