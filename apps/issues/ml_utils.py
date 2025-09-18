ML_TO_DJANGO_ISSUE_TYPE = {
    "garbage": "Garbage",
    "potholes": "Potholes",
    "street_light": "Street Light",
    "water_leakage": "Water Leakage",
    "not_labelled": "Not Labelled"
}

def map_ml_label_to_django(label):
    return ML_TO_DJANGO_ISSUE_TYPE.get(label, "Not Labelled")
import tensorflow as tf
from PIL import Image
import numpy as np

MODEL_PATH = '/usr/src/app/ML/issue_classifier.keras'
CLASS_NAMES = ['garbage', 'potholes', 'street_light', 'water_leakage']

def predict_issue_type(image_path, threshold=0.6):
    model = tf.keras.models.load_model(MODEL_PATH)
    img = Image.open(image_path).convert('RGB').resize((128, 128))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape((1, 128, 128, 3))
    predictions = model.predict(img_array)
    pred_idx = np.argmax(predictions)
    confidence = np.max(predictions)
    print(f"Predicted class: {CLASS_NAMES[pred_idx]}, Confidence: {confidence:.2f}")  # <-- Add this line
    if confidence < threshold:
        return 'not_labelled'
    return CLASS_NAMES[pred_idx]