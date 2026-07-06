from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template, request, send_from_directory, url_for
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
MODEL_PATH = BASE_DIR / "models" / "sklearn_logreg.joblib"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg"}
IMG_SIZE = (64, 64)
MAX_UPLOAD_SIZE_MB = 5
UPLOAD_RETENTION_MINUTES = 60

UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE_MB * 1024 * 1024


def cleanup_uploads(folder=UPLOAD_FOLDER, minutes=UPLOAD_RETENTION_MINUTES):
    """Remove old uploaded images so the uploads folder stays lightweight."""
    cutoff = datetime.now() - timedelta(minutes=minutes)
    for path in folder.iterdir():
        if path.is_file() and path.name != ".gitkeep":
            modified_at = datetime.fromtimestamp(path.stat().st_mtime)
            if modified_at < cutoff:
                path.unlink(missing_ok=True)


def load_model():
    """Load the trained scikit-learn model without changing model behavior."""
    if not MODEL_PATH.exists():
        raise SystemExit(f"Model file not found: {MODEL_PATH}")

    model_data = joblib.load(MODEL_PATH)
    return model_data["model"], list(model_data["classes"])


clf, classes = load_model()


def allowed_file(filename):
    """Check file extension before saving an upload."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_mime_type(file_storage):
    """Reject obvious non-image uploads before PIL validation."""
    return file_storage.mimetype in ALLOWED_MIME_TYPES


def build_upload_name(filename):
    """Create a sanitized, collision-resistant uploaded filename."""
    safe_name = secure_filename(filename)
    suffix = Path(safe_name).suffix.lower()
    stem = Path(safe_name).stem[:40] or "plant-image"
    return f"{stem}-{uuid4().hex[:10]}{suffix}"


def validate_image(path):
    """Verify the saved upload is a readable image file."""
    try:
        with Image.open(path) as image:
            image.verify()
    except (UnidentifiedImageError, OSError):
        path.unlink(missing_ok=True)
        raise ValueError("Please upload a valid JPG or PNG plant image.")


def predict_image(path):
    """Preprocess the image and run the existing trained model."""
    img = Image.open(path).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img).astype(np.float32) / 255.0
    feat = arr.flatten().reshape(1, -1)

    pred = clf.predict(feat)[0]
    if hasattr(clf, "predict_proba"):
        proba = clf.predict_proba(feat)[0]
        probs = {cls: float(probability) for cls, probability in zip(classes, proba)}
    else:
        probs = None

    return pred, probs


def build_confidence(probs):
    """Return the strongest class confidence as a percentage."""
    if not probs:
        return 0
    return round(max(probs.values()) * 100, 1)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if "file" not in request.files:
        return render_template("index.html", error="No file uploaded")

    file = request.files["file"]

    if file.filename == "":
        return render_template("index.html", error="No file selected")

    if not allowed_file(file.filename) or not allowed_mime_type(file):
        return render_template("index.html", error="Only JPG, JPEG, and PNG images are allowed.")

    filename = build_upload_name(file.filename)
    upload_path = Path(app.config["UPLOAD_FOLDER"]) / filename

    try:
        file.save(upload_path)
        validate_image(upload_path)
        cleanup_uploads()
        prediction, probabilities = predict_image(upload_path)
    except ValueError as exc:
        return render_template("index.html", error=str(exc))
    except Exception:
        upload_path.unlink(missing_ok=True)
        return render_template("index.html", error="Something went wrong while analyzing the image.")

    image_url = url_for("uploaded_file", filename=filename)
    confidence = build_confidence(probabilities)

    return render_template(
        "index.html",
        result=prediction,
        probs=probabilities,
        confidence=confidence,
        image_url=image_url,
        success="Image analyzed successfully.",
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error=f"File is too large. Please upload an image under {MAX_UPLOAD_SIZE_MB} MB.",
    ), 413


@app.errorhandler(404)
def page_not_found(error):
    return render_template("index.html", error="The requested page was not found."), 404


if __name__ == "__main__":
    print("Starting Weed Detection app...")
    app.run(debug=True)
