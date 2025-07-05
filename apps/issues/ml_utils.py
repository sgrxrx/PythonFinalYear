import tensorflow as tf
from PIL import Image
import numpy as np

MODEL_PATH = '/usr/src/app/ML/issue_classifier.keras'
CLASS_NAMES = ['garbage', 'potholes', 'street_light', 'water_leakage']

def predict_issue_type(image_path):
    model = tf.keras.models.load_model(MODEL_PATH)
    img = Image.open(image_path).convert('RGB').resize((128, 128))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape((1, 128, 128, 3))
    predictions = model.predict(img_array)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    return predicted_class