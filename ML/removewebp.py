import os
import glob

input_dir = 'dataset'
for class_dir in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_dir)
    if os.path.isdir(class_path):
        for webp_file in glob.glob(os.path.join(class_path, '*.webp')):
            os.remove(webp_file)
            print(f"Removed: {webp_file}")