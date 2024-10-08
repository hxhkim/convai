import openai
import json
import os
import pprint
from dotenv import load_dotenv
from typing import Dict, List
import glob
import time

load_dotenv()

MODEL = "gpt-4o-mini"
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai
client

def fill_empty_fields(data: Dict, messages: List[Dict]) -> Dict:
    messages_str = "\n".join([f"{msg['role']}: {msg['content']['text']}" for msg in messages])
    
    participant_1 = data['participant_persona']['participant_1']
    participant_2 = data['participant_persona']['participant_2']

    prompt = f"""Analyze the given Conversation Log and Participant information and fill in ONLY the missing fields in the original JSON format. Do not modify any existing information.:

    Participant 1:
    name: {participant_1['name']}
    age: {participant_1['age']}
    gender: {participant_1['gender']}
    personality: {participant_1['personality']}
    background: {participant_1['background']}

    Participant 2:
    name: {participant_2['name']}
    age: {participant_2['age']}
    gender: {participant_2['gender']}
    personality: {participant_2['personality']}
    background: {participant_2['background']}

    # Conversation Log:
    {messages_str}

    # Guidelines:
    1. Infer age, gender, and other details based on the text content and writing style.
    2. Generate diverse and unique names and personalities for each participant. Use various expressions, not using the same expressions repeatedly.
    3. Use str sentences for the personality and background fields.
    4. Keep use the original fields text if it exists."""

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
                return

            for key, value in filled_data.items():
                if key == 'Participant 1':
                    participant_1.update(value)
                elif key == 'Participant 2':
                    participant_2.update(value)
            
            data['participant_persona']['participant_1'] = participant_1
            data['participant_persona']['participant_2'] = participant_2

            return data
        except openai.error.Timeout as e:
            print(f"Attempt {attempt + 1} of {retries} failed with timeout. Retrying...")
            time.sleep(3)  # Wait for 3 seconds before retrying

    raise Exception("All retry attempts failed due to timeout.")



# # export_2018-07-04_train

# json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/export_2018-07-04_train/*.json'))


# for i, json_file in enumerate(json_files):
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#         messages = data['messages']

#     filled_data = fill_empty_fields(data, data['messages'])
#     print(f"filled_data_export_2018-07-04_train_{i + 1}:", filled_data)
#     print("=====================================")

#     output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-04_train'
#     output_file = os.path.join(output_dir, f'filled_data_export_2018-07-04_train_{i + 1}.json')

#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(filled_data, file, ensure_ascii=False, indent=4)


# # export_2018-07-05_train

# json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/export_2018-07-05_train/*.json'))


# for i, json_file in enumerate(json_files):
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#         messages = data['messages']

#     filled_data = fill_empty_fields(data, data['messages'])
#     print(f"filled_data_export_2018-07-05_train_{i + 1}:", filled_data)
#     print("=====================================")

#     output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-05_train'
#     output_file = os.path.join(output_dir, f'filled_data_export_2018-07-05_train_{i + 1}.json')

#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(filled_data, file, ensure_ascii=False, indent=4)




# # export_2018-07-06_train

# json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/export_2018-07-06_train/*.json'))


# for i, json_file in enumerate(json_files):
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#         messages = data['messages']

#     filled_data = fill_empty_fields(data, data['messages'])
#     print(f"filled_data_export_2018-07-06_train_{i + 1}:", filled_data)
#     print("=====================================")

#     output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-06_train'
#     output_file = os.path.join(output_dir, f'filled_data_export_2018-07-06_train_{i + 1}.json')

#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(filled_data, file, ensure_ascii=False, indent=4)


# # export_2018-07-07_train

# json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/export_2018-07-07_train/*.json'))


# for i, json_file in enumerate(json_files):
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#         messages = data['messages']

#     filled_data = fill_empty_fields(data, data['messages'])
#     print(f"filled_data_export_2018-07-07_train_{i + 1}:", filled_data)
#     print("=====================================")

#     output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-07_train'
#     output_file = os.path.join(output_dir, f'filled_data_export_2018-07-07_train_{i + 1}.json')

#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(filled_data, file, ensure_ascii=False, indent=4)


# # intermediate

# json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/intermediate/*.json'))


# for i, json_file in enumerate(json_files):
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#         messages = data['messages']

#     filled_data = fill_empty_fields(data, data['messages'])
#     print(f"filled_data_intermediate_{i + 1}:", filled_data)
#     print("=====================================")

#     output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/intermediate'
#     output_file = os.path.join(output_dir, f'filled_data_intermediate_{i + 1}.json')

#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(filled_data, file, ensure_ascii=False, indent=4)


# summer_wild_evaluation_dialogs

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/summer_wild_evaluation_dialogs/*.json'))

# open ai runtime out 에러로 잠시 홀드. summer_wild_evaluation_dialogs_1 ~ 2357 까지만 진행됨. 전체 갯수는 3495개임.
# 끝까지 진행 완료

for i, json_file in enumerate(json_files[2354:], start=2355):
    with open(json_file, 'r') as file:
        data = json.load(file)
        messages = data['messages']

    filled_data = fill_empty_fields(data, data['messages'])
    print(f"filled_data_summer_wild_evaluation_dialogs_{i + 1}:", filled_data)
    print(f"Function end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/summer_wild_evaluation_dialogs'
    output_file = os.path.join(output_dir, f'filled_data_summer_wild_evaluation_dialogs_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)



# # tolokers

# json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/tolokers/*.json'))

# # open ai runtime out 에러로 잠시 홀드. tolokers_1 ~ 219 까지만 진행되어 끝까지 다시 돌림.

# for i, json_file in enumerate(json_files[219:], start=220):
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#         messages = data['messages']

#     filled_data = fill_empty_fields(data, data['messages'])
#     print(f"filled_data_tolokers_{i + 1}:", filled_data)
#     print("=====================================")

#     output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/tolokers'
#     output_file = os.path.join(output_dir, f'filled_data_tolokers_{i + 1}.json')

#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(filled_data, file, ensure_ascii=False, indent=4)



# # volunteers

# json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/02_transformed_data/volunteers/*.json'))


# for i, json_file in enumerate(json_files):
#     with open(json_file, 'r') as file:
#         data = json.load(file)
#         messages = data['messages']

#     filled_data = fill_empty_fields(data, data['messages'])
#    print(f"filled_data_volunteers_{i + 1}:", filled_data)
#    print("=====================================")

#     output_dir = '/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/volunteers'
#     output_file = os.path.join(output_dir, f'filled_data_volunteers_{i + 1}.json')

#     with open(output_file, 'w', encoding='utf-8') as file:
#         json.dump(filled_data, file, ensure_ascii=False, indent=4)