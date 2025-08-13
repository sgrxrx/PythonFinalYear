import os
import glob

input_dir = 'dataset'
image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif')

for class_dir in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_dir)
    if os.path.isdir(class_path):
        count = 0
        for ext in image_extensions:
            count += len(glob.glob(os.path.join(class_path, ext)))
        print(f"{class_dir}: {count} images")