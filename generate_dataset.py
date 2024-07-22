from PIL import Image, ImageDraw
import random
import math
import numpy as np
import os

for path in [
    "datasets/dataset/train/stage_1/img", "datasets/dataset/train/stage_1/mask",
    "datasets/dataset/val/stage_1/img", "datasets/dataset/val/stage_1/mask",
    "datasets/dataset/train/stage_2/img", "datasets/dataset/train/stage_2/mask",
    "datasets/dataset/val/stage_2/img", "datasets/dataset/val/stage_2/mask",
    "datasets/dataset/train/stage_3/img", "datasets/dataset/train/stage_3/mask",
    "datasets/dataset/val/stage_3/img", "datasets/dataset/val/stage_3/mask",
    "datasets/dataset/train/stage_4/img", "datasets/dataset/train/stage_4/mask",
    "datasets/dataset/val/stage_4/img", "datasets/dataset/val/stage_4/mask",
    "datasets/dataset/train/stage_5/img", "datasets/dataset/train/stage_5/mask",
    "datasets/dataset/val/stage_5/img", "datasets/dataset/val/stage_5/mask",
    "datasets/dataset/train/stage_6/img", "datasets/dataset/train/stage_6/mask",
    "datasets/dataset/val/stage_6/img", "datasets/dataset/val/stage_6/mask",
]:
    if not os.path.exists(path):
        os.makedirs(path)


def generate_image(width=256, height=256, num_rectangles=7, image_path="", mask_path="", filename='generated_image.png',
                   noise_type=None, noise_intensity=0.1):
    # Размеры изображения
    # width = 512
    # height = 512
    image_path = "datasets/" + image_path
    mask_path = "datasets/" + mask_path

    # Цвета (RGB)
    forest = int(16.04796875), int(39.6009375), int(22.95046875)
    target = int(67.49166666666666), int(113.73333333333333), int(76.91166666666666)

    def add_noise(image, noise_type='all', intensity=0.1):
        img_array = np.array(image)

        if noise_type == 'background' or noise_type == 'all':
            mask = np.all(img_array == forest, axis=-1)
            noise = np.random.normal(0, intensity * 255, img_array.shape)
            img_array[mask] = np.clip(img_array[mask] + noise[mask], 0, 255).astype(np.uint8)

        if noise_type == 'target' or noise_type == 'all':
            mask = np.all(img_array == target, axis=-1)
            noise = np.random.normal(0, intensity * 255, img_array.shape)
            img_array[mask] = np.clip(img_array[mask] + noise[mask], 0, 255).astype(np.uint8)

        return Image.fromarray(img_array)

    # Создаем новое изображение с заданным фоном
    image = Image.new('RGB', (width, height), forest)
    mask = Image.new('RGB', (width, height), (0, 0, 0))

    # Создаем объект для рисования
    draw = ImageDraw.Draw(image)
    mask_draw = ImageDraw.Draw(mask)

    def rotate_point(x, y, cx, cy, angle):
        """Вращает точку (x, y) вокруг центра (cx, cy) на угол angle (в радианах)"""
        new_x = cx + (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle)
        new_y = cy + (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle)
        return new_x, new_y

    # Количество прямоугольников (может быть любым числом)
    # num_rectangles = 13

    # Вычисляем количество строк и столбцов
    rows = math.ceil(math.sqrt(num_rectangles))
    cols = math.ceil(num_rectangles / rows)

    # Размеры секции
    section_width = width // cols
    section_height = height // rows

    # Добавляем прямоугольники
    for i in range(num_rectangles):
        # Определяем, в какой секции будет прямоугольник
        row = i // cols
        col = i % cols

        # Определяем границы секции
        section_x = col * section_width
        section_y = row * section_height

        # Случайные координаты для прямоугольника внутри секции
        x = random.randint(section_x, section_x + section_width - 50)
        y = random.randint(section_y, section_y + section_height - 50)
        w = random.randint(30, min(50, section_width - (x - section_x)))
        h = random.randint(30, min(50, section_height - (y - section_y)))

        # Случайный угол поворота в радианах
        angle = random.uniform(0, 2 * math.pi)

        # Вычисляем центр прямоугольника
        cx, cy = x + w / 2, y + h / 2

        # Вращаем углы прямоугольника
        points = [
            rotate_point(x, y, cx, cy, angle),
            rotate_point(x + w, y, cx, cy, angle),
            rotate_point(x + w, y + h, cx, cy, angle),
            rotate_point(x, y + h, cx, cy, angle)
        ]

        # Рисуем повернутый прямоугольник
        draw.polygon(points, fill=target)
        mask_draw.polygon(points, fill=(255, 255, 255))

    # Выбираем случайный угол поворота для всего изображения
    rotation_angle = random.choice([0, 90, 180, 270])

    # Поворачиваем все изображение
    rotated_image = image.rotate(rotation_angle, expand=False)
    rotated_mask = mask.rotate(rotation_angle, expand=False)

    # Добавляем шум
    if noise_type:
        rotated_image = add_noise(rotated_image, noise_type, noise_intensity)

    # Сохраняем изображение
    rotated_image.save(image_path + filename)
    rotated_mask.save(mask_path + filename)


for i in range(100):
    # for i in range(10):
    generate_image(image_path="dataset/train/stage_1/img/", mask_path="dataset/train/stage_1/mask/",
                   filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15))
for i in range(100 // 5):
    # for i in range(10//5):
    generate_image(image_path="dataset/val/stage_1/img/", mask_path="dataset/val/stage_1/mask/", filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15))

for i in range(500):
    # for i in range(10):
    generate_image(image_path="dataset/train/stage_2/img/", mask_path="dataset/train/stage_2/mask/",
                   filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="background",
                   noise_intensity=random.uniform(0.03, 0.08))
for i in range(500 // 5):
    # for i in range(10//5):
    generate_image(image_path="dataset/val/stage_2/img/", mask_path="dataset/val/stage_2/mask/", filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="background",
                   noise_intensity=random.uniform(0.03, 0.08))

for i in range(1000):
    # for i in range(10):
    generate_image(image_path="dataset/train/stage_3/img/", mask_path="dataset/train/stage_3/mask/",
                   filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="target",
                   noise_intensity=random.uniform(0.03, 0.08)
                   )
for i in range(1000 // 5):
    # for i in range(10//5):
    generate_image(image_path="dataset/val/stage_3/img/", mask_path="dataset/val/stage_3/mask/", filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="target",
                   noise_intensity=random.uniform(0.03, 0.08)
                   )

for i in range(5000):
    # for i in range(10):
    generate_image(image_path="dataset/train/stage_4/img/", mask_path="dataset/train/stage_4/mask/",
                   filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="all",
                   noise_intensity=random.uniform(0.15, 0.3)
                   # noise_intensity=1
                   )
for i in range(5000 // 5):
    # for i in range(10//5):
    generate_image(image_path="dataset/val/stage_4/img/", mask_path="dataset/val/stage_4/mask/", filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="all",
                   noise_intensity=random.uniform(0.15, 0.3)
                   # noise_intensity=1
                   )

for i in range(20000):
    # for i in range(10):
    generate_image(image_path="dataset/val/stage_5/img/", mask_path="dataset/val/stage_5/mask/", filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="all",
                   noise_intensity=random.uniform(0.3, 0.6)
                   )
for i in range(20000 // 5):
    # for i in range(10//5):
    generate_image(image_path="dataset/train/stage_5/img/", mask_path="dataset/train/stage_5/mask/",
                   filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="all",
                   noise_intensity=random.uniform(0.3, 0.6)
                   )

for i in range(50000):
    # for i in range(10):
    generate_image(image_path="dataset/train/stage_6/img/", mask_path="dataset/train/stage_6/mask/",
                   filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="all",
                   noise_intensity=random.uniform(0.6, 1)
                   )
for i in range(50000 // 5):
    # for i in range(10//5):
    generate_image(image_path="dataset/val/stage_6/img/", mask_path="dataset/val/stage_6/mask/", filename=f"{i}.png",
                   num_rectangles=random.randint(5, 15), noise_type="all",
                   noise_intensity=random.uniform(0.6, 1)
                   )

# dataset/
# ├── train/
#     ├── stage_1/
#         ├── img/
#             ├── 0.png
#             ├── 1.png
#             ...
#         └── mask/
#             ├── 0.png
#             ├── 1.png
#             ...
#     ├── stage_2/
#         ├── img/
#             ├── 0.png
#             ├── 1.png
#             ...
#         └── mask/
#             ├── 0.png
#             ├── 1.png
#             ...
#     ...
#     └── stage6/
#         ├── img/
#             ├── 0.png
#             ├── 1.png
#             ...
#         └── mask/
#             ├── 0.png
#             ├── 1.png
#             ...
# └── val/
#     ├── stage_1/
#         ├── img/
#             ├── 0.png
#             ├── 1.png
#             ...
#         └── mask/
#             ├── 0.png
#             ├── 1.png
#             ...
#     ├── stage_2/
#         ├── img/
#             ├── 0.png
#             ├── 1.png
#             ...
#         └── mask/
#             ├── 0.png
#             ├── 1.png
#             ...
#     ...
#     └── stage6/
#         ├── img/
#             ├── 0.png
#             ├── 1.png
#             ...
#         └── mask/
#             ├── 0.png
#             ├── 1.png
#             ...
