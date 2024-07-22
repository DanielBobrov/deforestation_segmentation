from ultralytics import YOLO

# Загрузка предобученной модели YOLOv8
model = YOLO('yolov8n-seg.pt')  # или другая модель, например 'yolov8s-seg.pt'

# Обучение на каждой стадии
for stage in range(1, 7):  # предполагаем, что у вас 6 стадий
    print(f"Training on stage {stage}")

    # Путь к файлу конфигурации датасета для текущей стадии
    data_yaml = f'configs/dataset_stage_{stage}.yaml'

    # Обучение модели
    results = model.train(
        data=data_yaml,
        epochs=100,  # количество эпох
        imgsz=256,  # размер изображения
        batch=16,  # размер батча
        name=f'yolov8_stage_{stage}'  # имя для сохранения результатов
    )

    # Сохранение модели после каждой стадии
    model.save(f'yolov8_stage_{stage}.pt')

print("Training completed for all stages")
