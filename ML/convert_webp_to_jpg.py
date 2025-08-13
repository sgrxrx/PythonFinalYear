from PIL import Image
import os
import glob

input_dir = 'dataset'
for class_dir in os.listdir(input_dir):
    class_path = os.path.join(input_dir, class_dir)
    if os.path.isdir(class_path):
        for webp_file in glob.glob(os.path.join(class_path, '*.webp')):
            img = Image.open(webp_file).convert('RGB')
            new_file = webp_file.rsplit('.', 1)[0] + '.jpg'
            img.save(new_file, 'JPEG')