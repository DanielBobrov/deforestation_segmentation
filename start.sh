#!/bin/bash

python3 generate_dataset.py
echo "dataset generated"
python3 generate_labels.py
echo "labels generated"
python3 generate_configs.py
echo "configs generated"
python3 train_model.py
echo "model trained"
