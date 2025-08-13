import os
from PIL import Image

dataset_dir = 'dataset'  # or your actual dataset path

for class_dir in os.listdir(dataset_dir):
    class_path = os.path.join(dataset_dir, class_dir)
    if os.path.isdir(class_path):
        for fname in os.listdir(class_path):
            fpath = os.path.join(class_path, fname)
            try:
                with Image.open(fpath) as img:
                    img.verify()
            except Exception:
                print(f"Removing corrupted or invalid file: {fpath}")
                os.remove(fpath)