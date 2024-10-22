from openai import OpenAI
from openai import RateLimitError
from openai import APITimeoutError
from openai import APIConnectionError
from openai import APIError
from openai import AuthenticationError

import json
import os
from typing import Dict, List
import re
import shutil
import time

MODEL = "gpt-4o-mini"
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def label_emotion(participant_data:str, message_data: str, message_log_data: Dict) -> Dict:

    # step 1. generate prompt
    id = message_data.get('id', {})
    content = message_data.get('content', {})
    if not content.get('emotion_scores') and 'text' in content:
        text = content['text']
        prompt = f"""Analyze the following text and provide emotion_scores field for the following categories: Anger, Fear, Joy, Sadness, Surprise, Love, Boredom, Neutral. The output should be in JSON format with the emotion categories as keys and their respective scores as values, totaling exactly 100. 

        # Guidelines:
        1. Consider the Participant Information and Conversation Log when interpreting the emotional content of the text.
        2. Subtle emotional cues should be reflected in the corresponding emotion scores, but don't overinterpret.
        3. Assign a very high score to that emotion category when there is clear and strong evidence of a specific emotion in the text.

        # Expected output example:
        "emotion_scores": {{
            "Anger": ,
            "Fear": ,
            "Joy": ,
            "Sadness": 
            "Surprise": ,
            "Love": ,
            "Boredom": ,
            "Neutral": 
        }},
        "text": "{text}"

        # Participant Information: 
        {participant_data},

        # Conversation Log:
        {message_log_data}

        Ensure that your scoring reflects the intensity and clarity of the emotional expression in the text."""

        print(prompt)
        print("=====================================")

        # step 2. call OpenAI API
        retries = 3
        for attempt in range(retries):
            try:
                start_time = time.time()
                response = client.chat.completions.create(
                            model=MODEL,
                            messages=[
                                {"role": "system", "content": "You are an AI assistant that helps to build conversation data set."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.8,
                            response_format={"type": "json_object"}
                        )
                end_time = time.time()
            
                print(f"message id: {id}")
                print(f"message: {text}")
                print(f"API call took {end_time - start_time} seconds")
                print("=====================================")

                response_content = response.choices[0].message.content
                print(f"response_content: {response_content}")
                print("=====================================")

                try:
                    response_content = json.loads(response_content)  
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                    continue

                if 'content' not in message_data or not isinstance(message_data['content'], dict):
                    return message_data

                if message_data.get('content', {}).get('text') == text:
                    message_data['content']['emotion_scores'] = response_content['emotion_scores']
                    print(f"content: {content}")
                    print(f"Updated message_data: {message_data}")
                    print("=====================================")

                break

            except (APITimeoutError, APIConnectionError, APIError, AuthenticationError) as e:
                print(f"Attempt {attempt + 1} of {retries} failed with {e}. Retrying...")
                time.sleep(3) 
        else:
            print(f"Failed to process message {id}: {text}")

    return message_data



def process_files(input_directory_path: str, output_directory_path: str, message_files: List[str] = None):

    # load data from input directory

    # participant data
    participant_filename = "participant.json"
    participant_file_path = os.path.join(input_directory_path, participant_filename)

    with open(participant_file_path, 'r', encoding='utf-8') as file:
        participant_data = json.load(file)
    print(participant_data)
    print("---------------------------------")

    # message data and message log data
    message_files = sorted([f for f in os.listdir(input_directory_path) if f.startswith("message") and f.endswith(".json")])
    message_log_data = []

    for message_filename in message_files:
        message_file_path = os.path.join(input_directory_path, message_filename)
        with open(message_file_path, 'r', encoding='utf-8') as file:
            message_data = json.load(file)
            message_log_data.append(message_data)

            # Keep only the latest 100 messages for saving tokens
            if len(message_log_data) > 100:
                message_log_data.pop(0)

            print(f"message_data: {message_data}")
            print(f"message_log_data: {message_log_data}")
            print("=====================================")

            # call label_emotion function
            start_time = time.time()
            message_data = label_emotion(participant_data, message_data, message_log_data)
            end_time = time.time()

            print(f"Processing {message_filename} took {end_time - start_time} seconds")
            print(f"final_data_{message_filename}:", message_data)
            print("=====================================")

            # save the updated message data to the output directory
            shutil.copy(participant_file_path, output_directory_path) # copy participant.json to the output directory
            output_message_file_path = os.path.join(output_directory_path, message_filename)

            try: 
                with open(output_message_file_path, 'w', encoding='utf-8') as file:
                    json.dump(message_data, file, ensure_ascii=False, indent=4)

                print(f"participant.json copied to {output_directory_path}")
                print(f"{message_filename} saved to {output_message_file_path}")
            
            except:
                print(f"Failed to save {message_filename} to {output_message_file_path}")     
                continue     
    return 



def process_all_folders(file_numbers: List[str], dataset: str, data_state: str, folder_name: str):
    for file_number in file_numbers:
        input_directory_path = f"{base_directory_path}/{dataset}_{data_state}_{folder_name}_{file_number}"
        output_directory_path = f"{base_directory_path}/{dataset}_{data_state}_{folder_name}_{file_number}"

        print("input_directory_path:", input_directory_path)
        print("output_directory_path:", output_directory_path)
        print("=====================================")

        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)
        process_files(input_directory_path, output_directory_path)
        print(f"Processed files for {dataset}_{data_state}_{folder_name}_{file_number}")



def count_empty_fields(base_directory_path: str):
    # Initialize lists to store the directory paths and the full file paths of files with empty emotion_scores
    empty_file_paths = []
    empty_emotion_files = []

    # Traverse the directory
    for root, dirs, files in os.walk(base_directory_path):
        for file in sorted(files):
            if file.startswith("message_") and file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if not data.get("content", {}).get("emotion_scores"):
                        empty_emotion_files.append(file_path)
                        empty_file_paths.append(root)

    empty_emotion_files = sorted(empty_emotion_files)
    empty_file_paths = sorted(set(empty_file_paths))  # Remove duplicates and sort


    for path, file in zip(empty_file_paths, empty_emotion_files):
        print(path)
        print(file)

    # If there are more paths than files or vice versa, print the remaining items
    if len(empty_file_paths) > len(empty_emotion_files):
        for path in empty_file_paths[len(empty_emotion_files):]:
            print(path)
    elif len(empty_emotion_files) > len(empty_file_paths):
        for file in empty_emotion_files[len(empty_file_paths):]:
            print(file)

    print(f"Total files with empty emotion_scores: {len(empty_emotion_files)}")
    print(f"Total directories with empty emotion_scores: {len(empty_file_paths)}")

    return empty_file_paths, empty_emotion_files



def re_process_files(input_directory_path: str, output_directory_path: str, message_files: List[str] = None):

    # load data from input directory

    # participant data
    participant_filename = "participant.json"
    participant_file_path = os.path.join(input_directory_path, participant_filename)

    with open(participant_file_path, 'r', encoding='utf-8') as file:
        participant_data = json.load(file)
    print(participant_data)
    print("---------------------------------")

    # message data and message log data
    # message_files = sorted([f for f in os.listdir(input_directory_path) if f.startswith("message") and f.endswith(".json")])
    message_log_data = []

    for message_filename in message_files:
        message_file_path = os.path.join(input_directory_path, message_filename)
        with open(message_file_path, 'r', encoding='utf-8') as file:
            message_data = json.load(file)
            message_log_data.append(message_data)

            # Keep only the latest 100 messages for saving tokens
            if len(message_log_data) > 100:
                message_log_data.pop(0)

            print(f"message_data: {message_data}")
            print(f"message_log_data: {message_log_data}")
            print("=====================================")

            # call label_emotion function
            start_time = time.time()
            message_data = label_emotion(participant_data, message_data, message_log_data)
            end_time = time.time()

            print(f"Processing {message_filename} took {end_time - start_time} seconds")
            print(f"final_data_{message_filename}:", message_data)
            print("=====================================")

            # # save the updated message data to the output directory
            # shutil.copy(participant_file_path, output_directory_path) # copy participant.json to the output directory
            # print(f"participant.json copied to {output_directory_path}")

            output_message_file_path = os.path.join(output_directory_path, message_filename)

            try: 
                with open(output_message_file_path, 'w', encoding='utf-8') as file:
                    json.dump(message_data, file, ensure_ascii=False, indent=4)

                
                print(f"{message_filename} saved to {output_message_file_path}")
            
            except:
                print(f"Failed to save {message_filename} to {output_message_file_path}")     
                continue     
    return 



if __name__ == "__main__":

    dataset = "convai"
    data_state = "emotion_labeled_data"
    folder_name = "export_2018-07-07_train"

    base_directory_path = f"/home/ubuntu/conversation-data/dataset-01-convai/convai/data/05_final_data/{folder_name}"
    file_numbers = sorted([d.split('_')[-1] for d in os.listdir(base_directory_path) if os.path.isdir(os.path.join(base_directory_path, d))])

    # # Step 1: Run process_files once
    # process_all_folders(file_numbers, dataset, data_state, folder_name)
    
    # Step 2: Count empty fields and process files in a loop
    while True:
        empty_file_paths, empty_emotion_files = count_empty_fields(base_directory_path)
        if not empty_emotion_files:
            print("All fields are filled.")
            break
        else:
            print(f"Processing {len(empty_emotion_files)} files with empty fields...")
            # # Process only the first 10 files in the list for testing
            # current_file_paths = empty_file_paths[:10]
            # current_emotion_files = empty_emotion_files[:10]

            current_file_paths = empty_file_paths
            current_emotion_files = empty_emotion_files
            
            for file_path, emotion_file in zip(current_file_paths, current_emotion_files):
                output_directory_path = file_path  # assuming the output should be in the same directory
                
                # Ensure the output directory exists
                if not os.path.exists(output_directory_path):
                    os.makedirs(output_directory_path)
                
                re_process_files(file_path, output_directory_path, [emotion_file])
            
            print("Processing complete. Checking for remaining empty fields...")