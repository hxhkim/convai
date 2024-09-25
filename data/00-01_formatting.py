import json
import os

# raw data directory path
input_dir_path = '/home/user1/conversation-data/dataset-01-convai/data/00_raw_data'

# formatted data directory path
output_dir_path = '/home/user1/conversation-data/dataset-01-convai/data/01_formatted_data'

# directory creation if not exist
os.makedirs(output_dir_path, exist_ok=True)

# JSON file formatting for each file in the input directory
for filename in os.listdir(input_dir_path):
    if filename.endswith('.json'):

        # input and output file paths definition
        input_file_path = os.path.join(input_dir_path, filename)
        output_file_path = os.path.join(output_dir_path, f"formatted_{filename}")
        
        # JSON file read
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        
        # JSON data formatting
        formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
        
        # JSON file write
        with open(output_file_path, 'w') as file:
            file.write(formatted_json)
        
        print(f"Formatted JSON data has been saved to {output_file_path}")