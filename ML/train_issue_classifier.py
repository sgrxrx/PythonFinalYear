import os
import random
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, average_precision_score
import numpy as np

DATASET_DIR = 'dataset'
IMAGES_PER_CLASS = 1000
IMG_SIZE = (128, 128)

filepaths = []
labels = []
class_names = sorted(os.listdir(DATASET_DIR))
class_to_index = {name: idx for idx, name in enumerate(class_names)}

for class_name in class_names:
    class_dir = os.path.join(DATASET_DIR, class_name)
    if os.path.isdir(class_dir):
        images = [os.path.join(class_dir, f) for f in os.listdir(class_dir)
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
        sampled = random.sample(images, min(IMAGES_PER_CLASS, len(images)))
        filepaths.extend(sampled)
        labels.extend([class_to_index[class_name]] * len(sampled))

# Shuffle the dataset
combined = list(zip(filepaths, labels))
random.shuffle(combined)
filepaths[:], labels[:] = zip(*combined)

def process_path(file_path, label):
    def _load_image(path):
        try:
            img = tf.io.read_file(path)
            img = tf.image.decode_image(img, channels=3)
            img.set_shape([None, None, 3])
            img = tf.image.resize(img, IMG_SIZE)
            img = tf.cast(img, tf.float32) / 255.0
            return img
        except Exception:
            return tf.zeros([*IMG_SIZE, 3], dtype=tf.float32)
    img = tf.py_function(_load_image, [file_path], tf.float32)
    img.set_shape([*IMG_SIZE, 3])
    return img, label

ds = tf.data.Dataset.from_tensor_slices((list(filepaths), list(labels)))
ds = ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
ds = ds.filter(lambda img, label: tf.reduce_sum(img) > 0)
ds = ds.batch(32).prefetch(tf.data.AUTOTUNE)

# model = models.Sequential([
#     layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Flatten(),
#     layers.Dense(64, activation='relu'),
#     layers.Dense(len(class_names), activation='softmax')
# ])
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


# Split dataset into train and test for evaluation
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, average_precision_score
import numpy as np

split_idx = int(0.8 * len(filepaths))
train_files, test_files = filepaths[:split_idx], filepaths[split_idx:]
train_labels, test_labels = labels[:split_idx], labels[split_idx:]

train_ds = tf.data.Dataset.from_tensor_slices((list(train_files), list(train_labels)))
train_ds = train_ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
train_ds = train_ds.filter(lambda img, label: tf.reduce_sum(img) > 0)
train_ds = train_ds.batch(32).prefetch(tf.data.AUTOTUNE)

test_ds = tf.data.Dataset.from_tensor_slices((list(test_files), list(test_labels)))
test_ds = test_ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE)
test_ds = test_ds.filter(lambda img, label: tf.reduce_sum(img) > 0)
test_ds = test_ds.batch(32).prefetch(tf.data.AUTOTUNE)

model.fit(train_ds, epochs=70)
model.save('issue_classifier.keras')

# Evaluation
y_true = []
y_pred = []
y_score = []
for images, labels in test_ds:
    preds = model.predict(images)
    y_true.extend(labels.numpy())
    y_pred.extend(np.argmax(preds, axis=1))
    y_score.extend(preds)

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred, average='weighted', zero_division=0))
print("Recall:", recall_score(y_true, y_pred, average='weighted', zero_division=0))
print("F1 Score:", f1_score(y_true, y_pred, average='weighted', zero_division=0))
try:
    print("MAP:", average_precision_score(
        tf.keras.utils.to_categorical(y_true, num_classes=len(class_names)),
        np.array(y_score), average='macro'))
except Exception as e:
    print("MAP calculation error:", e)