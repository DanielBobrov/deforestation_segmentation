import os

for path in [
    "configs"
]:
    if not os.path.exists(path):
        os.makedirs(path)

for i in range(1, 7):
    with open(f"configs/dataset_stage_{i}.yaml", "w") as f:
        print(f"""path: dataset
train: train/stage_{i}/img
val: val/stage_{i}/img
nc: 1
names: ['object']

# Опционально, если у вас есть тестовый набор
# test: test/stage_1/img""", file=f)
