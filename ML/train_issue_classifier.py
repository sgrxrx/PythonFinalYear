import tensorflow as tf
from tensorflow.keras import layers, models

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(4, activation='softmax')  # 5 classes for your issue types
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    'dataset/',
    image_size=(128, 128),
    batch_size=32,
    label_mode='int'  # for sparse_categorical_crossentropy
)

# Train the model
model.fit(train_ds, epochs=10)

# Save the trained model
model.save('issue_classifier.keras')