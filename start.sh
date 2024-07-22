#!/bin/bash

python generate_dataset.py
python generate_labels.py
python generate_configs.py
python train_model.py
