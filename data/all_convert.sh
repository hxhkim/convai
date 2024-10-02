#!/bin/bash
# bash all_transfer.sh
# nohup bash all_transfer.sh &

# Navigate to the directory containing the Python scripts
cd /home/user1/conversation-data/dataset-01-convai/data

# Execute the Python scripts in sequence
nohup python3 02-03_filling_fields_v2_timeout-debug.py &
nohup python3 03-04_emotion_labeling.py &