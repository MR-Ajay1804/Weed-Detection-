# Weed Detection AI

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web_App-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Portfolio_Ready-49e88c?style=for-the-badge)

A modern machine learning web application that classifies plant images as **weed** or **crop**. The project combines a Flask backend, a trained scikit-learn Logistic Regression model, secure image upload handling, and a responsive glassmorphism UI suitable for a final-year project or recruiter portfolio.

## Features

- Modern dark glassmorphism interface
- Animated gradient background and lightweight particle effect
- Drag-and-drop image upload
- Image preview before prediction
- JPG, JPEG, and PNG upload validation
- Secure filename handling
- File size limit and invalid image protection
- Loading state while prediction is running
- Confidence score with professional progress bar
- Clean prediction result card
- Reset button for quick retry
- Responsive navbar and footer
- Fully responsive desktop, tablet, and mobile layout
- Separate CSS and JavaScript files for maintainability

## 📷 Screenshots

### 🏠 Home Page

![Home Page](docs/screenshots/homepage.png)

---

### 📤 Image Upload

![Upload](docs/screenshots/upload.png)

---

### 🌿 Prediction Result

![Prediction Result](docs/screenshots/result.png)

## Tech Stack

- Python
- Flask
- scikit-learn
- NumPy
- Pillow
- joblib
- HTML
- CSS
- JavaScript

## Folder Structure

```text
weed-detection/
|-- app.py
|-- requirements.txt
|-- README.md
|-- train_sklearn.py
|-- static/
|   |-- css/
|   |   `-- styles.css
|   |-- js/
|   |   `-- app.js
|   `-- images/
|-- templates/
|   `-- index.html
|-- models/
|   `-- sklearn_logreg.joblib
|-- uploads/
|   `-- .gitkeep
|-- src/
|   |-- check_data.py
|   |-- infer_sklearn.py
|   `-- __init__.py
`-- data/
    |-- crop/
    `-- weed/
```

## Requirements

Install the dependencies from:

```bash
requirements.txt
```

Main packages:

- Flask
- joblib
- numpy
- Pillow
- scikit-learn

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/weed-detection-ai.git
cd weed-detection-ai
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Flask app:

```bash
python app.py
```

Open the local URL shown in the terminal:

```text
http://127.0.0.1:5000
```

Upload a plant image and click **Predict Image** to classify it.

## Command-Line Prediction

```bash
python src/infer_sklearn.py path/to/image.jpg
```

## Training

The trained model is already stored in:

```text
models/sklearn_logreg.joblib
```

To retrain the model, arrange the dataset like this:

```text
data/
|-- crop/
`-- weed/
```

Then run:

```bash
python train_sklearn.py
```

## Model Information

- Model type: Logistic Regression
- Library: scikit-learn
- Input image size: 64 x 64 RGB
- Preprocessing: resize, normalize pixel values, flatten image array
- Classes: weed and crop
- Saved model format: joblib

The prediction logic and trained model file are preserved. UI, validation, upload security, and maintainability were improved around the existing machine learning flow.

## Future Improvements

- Add CNN-based deep learning model for higher image accuracy
- Add dataset download link
- Add model evaluation charts
- Add deployment instructions for Render or Railway
- Add automated tests for Flask routes
- Add screenshot images in the `docs/` folder

## License

This project is available under the MIT License. Add a `LICENSE` file before publishing if you want to make the license official.

## Author

**Your Name**

- GitHub: `https://github.com/your-username`
- LinkedIn: `https://linkedin.com/in/your-profile`
