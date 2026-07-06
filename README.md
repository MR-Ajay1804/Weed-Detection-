# Weed Detection Project

A simple machine learning web app that classifies plant images as **weed** or **crop**. The project uses a trained scikit-learn logistic regression model and a Flask interface where users can upload an image and see the prediction with confidence.

## Features

- Upload JPG, JPEG, or PNG plant images
- Predict whether the image is a weed or crop
- Show prediction confidence when model probabilities are available
- Clean Flask web interface
- Separate scripts for training and command-line inference
- Safer upload handling with file type checks, file size limit, and automatic cleanup

## Tech Stack

- Python
- Flask
- scikit-learn
- NumPy
- Pillow
- joblib
- HTML, CSS, and JavaScript

## Project Structure

```text
weed-detection/
|-- app.py                       # Flask web application
|-- requirements.txt             # Python dependencies
|-- models/
|   `-- sklearn_logreg.joblib    # Trained model
|-- train_sklearn.py             # Model training script
|-- src/
|   |-- infer_sklearn.py         # Command-line prediction script
|   `-- check_data.py            # Dataset checking helper
|-- templates/
|   `-- index.html               # Web app page
|-- data/
|   |-- crop/                    # Crop training images
|   `-- weed/                    # Weed training images
`-- uploads/                     # Temporary uploaded images
```

## Dataset

The local dataset currently contains:

- 477 weed images
- 349 crop images
- 826 total images before augmentation

During training, each image is resized to 64 x 64 pixels, normalized, flattened, and augmented with a horizontal flip. The model is trained on an 80/20 train-test split.

The `data/` folder is ignored in Git because image datasets can make the repository large. Add a small sample dataset or share the dataset link separately if needed.

## How It Works

1. Images are loaded from `data/weed` and `data/crop`.
2. Each image is resized to 64 x 64 RGB pixels.
3. Pixel values are normalized between 0 and 1.
4. The image is flattened into a feature vector.
5. A logistic regression classifier is trained using scikit-learn.
6. The trained model is saved in `models/sklearn_logreg.joblib`.
7. The Flask app loads the saved model and predicts uploaded images.

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Web App

```bash
python app.py
```

Open the local address shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

## Train the Model

Make sure your dataset is arranged like this:

```text
data/
|-- crop/
`-- weed/
```

Then run:

```bash
python train_sklearn.py
```

## Predict from Command Line

```bash
python src/infer_sklearn.py path/to/image.jpg
```

## What I Used in This Project

This project uses Python for the backend and machine learning pipeline, Flask for the web app, scikit-learn for the logistic regression classifier, Pillow and NumPy for image preprocessing, and joblib to save and load the trained model. The frontend is built with HTML, CSS, and JavaScript.

## Notes for GitHub

- Do not push `venv/`, `uploads/`, or `__pycache__/`.
- Keep the trained model if you want the app to run immediately after cloning.
- Keep the dataset outside Git, or upload it separately and mention the download link in this README.
- Before pushing, run the app once and test one weed image and one crop image.
