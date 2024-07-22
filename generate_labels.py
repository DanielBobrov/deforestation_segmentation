import os
import cv2
import numpy as np
import shutil


def mask_to_yolo_seg(mask_path, img_path, output_path):
    mask = cv2.imread(mask_path, 0)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    with open(output_path, 'w') as f:
        for cnt in contours:
            f.write("0 ")
            for point in cnt.reshape(-1, 2):
                x, y = point
                x_norm = x / w
                y_norm = y / h
                f.write(f"{x_norm:.6f} {y_norm:.6f} ")
            f.write("\n")


def process_directory(input_dir, output_dir):
    images_dir = os.path.join(output_dir, 'img')
    # labels_dir = os.path.join(output_dir, 'labels')

    os.makedirs(images_dir, exist_ok=True)
    # os.makedirs(labels_dir, exist_ok=True)

    for filename in os.listdir(os.path.join(input_dir, 'img')):
        if filename.endswith('.png'):
            img_path = os.path.join(input_dir, 'img', filename)
            mask_path = os.path.join(input_dir, 'mask', filename)
            output_img_path = os.path.join(images_dir, filename)
            output_label_path = os.path.join(images_dir, os.path.splitext(filename)[0] + '.txt')

            # Копируем изображение
            # shutil.copy2(img_path, output_img_path)

            # Конвертируем и сохраняем маску
            mask_to_yolo_seg(mask_path, img_path, output_label_path)


# Обработка всех стадий и наборов данных
base_dir = 'datasets/dataset'
for dataset in ['train', 'val']:
    for stage in range(1, 7):
        input_dir = os.path.join(base_dir, dataset, f'stage_{stage}')
        output_dir = os.path.join(base_dir, dataset, f'stage_{stage}')

        process_directory(input_dir, output_dir)

print("Conversion completed")
