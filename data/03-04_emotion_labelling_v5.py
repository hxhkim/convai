import openai
import json
import os
from dotenv import load_dotenv
from typing import Dict, List
import re
import shutil


load_dotenv()

MODEL = "gpt-4o-mini"
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai


# folder_names = ["export_2018-07-04_train", 
#                 "export_2018-07-05_train", 
#                 "export_2018-07-06_train", 
#                 "export_2018-07-07_train", 
#                 "intermediate", 
#                 "summer_wild_evaluation_dialogs", 
#                 "tolokers", 
#                 "volunteers"]

folder_names = ["export_2018-07-05_train", 
                "export_2018-07-06_train", 
                "export_2018-07-07_train", ]

dataset = "convai"
data_state = "emotion_labeled_data"
# folder_name = "export_2018-07-04_train"
# input_directory_path = f"/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/{folder_name}"
# output_directory_path = f"/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/{folder_name}"
except_directory_path = f"/home/user1/conversation-data/dataset-01-convai/data/except"


def label_emotion(data: Dict, messages: List[Dict]) -> Dict:
    for message in data['messages']:
        content = message.get('content', {})
        if not content.get('emotion_scores') and 'text' in content:
            text = content['text']
            prompt = f"""Analyze the following text and provide emotion_scores field for the following categories: Anger, Fear, Joy, Sadness, Surprise, Love, Boredom, Neutral. The output should be in JSON format with the emotion categories as keys and their respective scores as values, totaling exactly 100. 

            # Guidelines:
            1. Consider the Participant Information and Conversation Log when interpreting the emotional content of the text.
            2. Subtle emotional cues should be reflected in the corresponding emotion scores, but don't overinterpret.
            3. Assign a very high score to that emotion category when there is clear and strong evidence of a specific emotion in the text.

            # Participant Information: 
            {data["participant_persona"]},

            # Conversation Log:
            {data["messages"]}
        
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
            
            Ensure that your scoring reflects the intensity and clarity of the emotional expression in the text."""


            # openai timeout error retry
            retries = 3
            for attempt in range(retries):
                try:
                    response = client.ChatCompletion.create(
                                model=MODEL,
                                messages=[
                                    {"role": "system", "content": "You are an AI assistant that helps to build conversation data set."},
                                    {"role": "user", "content": prompt}
                                ],
                                temperature=0.8,
                                response_format={"type": "json_object"}
                            )

                    response_content = response.choices[0].message.content

                    try:
                        filled_data = json.loads(response_content)  
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError: {e}")
                        continue

                    if content.get('text') == text:
                        content['emotion_scores'] = filled_data.get('emotion_scores', {})

                    break

                except openai.error.Timeout as e:
                    print(f"Attempt {attempt + 1} of {retries} failed with timeout. Retrying...")
                    time.sleep(3) 
            else:
                print(f"Failed to process message: {text}")

    return data  



def handle_rate_limit_error(filename, source_directory, destination_directory):
    source_path = os.path.join(source_directory, filename)
    destination_path = os.path.join(destination_directory, filename)
    shutil.copy(source_path, destination_path)
    print(f"File {filename} copied to {destination_directory} due to RateLimitError.")


def process_files(file_list: List[str], input_directory_path: str, output_directory_path: str):
    for filename in file_list:
        input_file_path = os.path.join(input_directory_path, filename)
        try:
            with open(input_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Check if data is loaded correctly
            print(f"Processing file: {input_file_path}")
            print(f"Data: {data}")

            messages = data.get('messages', [])
            filled_data = label_emotion(data, messages)
            print(f"emotion_labeled_data_{filename}:", filled_data)
            print("=====================================")

            # Extract the number from the original file name
            match = re.search(r'_(\d{5})\.json$', filename)
            if match:
                file_number = match.group(1)
            else:
                raise ValueError(f"Filename {filename} does not match the expected pattern")

            output_filename = f"{dataset}_{data_state}_{folder_name}_{file_number}.json"
            output_file_path = os.path.join(output_directory_path, output_filename)
            os.makedirs(output_directory_path, exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                json.dump(filled_data, file, ensure_ascii=False, indent=4)

        except openai.error.RateLimitError:
            handle_rate_limit_error(filename, input_directory_path, except_directory_path)
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")


if __name__ == "__main__":
    for folder_name in folder_names:
        input_directory_path = f"/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/{folder_name}"
        output_directory_path = f"/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/{folder_name}"
        
        all_files = [f for f in os.listdir(input_directory_path) if f.endswith(".json")]
        all_files.sort()
        
        process_files(all_files, input_directory_path, output_directory_path, folder_name)