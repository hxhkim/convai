# 24. 09. 24.
# 각 폴더 별로 5개씩 테스트 완료
# 잘 변환되어 들어가는 것을 확인.
# sh 스크립트로도 잘 돌아가는 것을 확인.
# 최종 검수 후 전체 파일 돌리면 됨.

import openai
import json
import os
import pprint
from dotenv import load_dotenv
from typing import Dict, List
import glob

load_dotenv()

MODEL = "gpt-4o-mini"
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai

def label_emotion(data: Dict) -> Dict:
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

    return data



# export_2018-07-04_train

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-04_train/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_export_2018-07-04_train_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/export_2018-07-04_train'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_export_2018-07-04_train_v3_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)


# export_2018-07-05_train

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-05_train/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_export_2018-07-05_train_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/export_2018-07-05_train'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_export_2018-07-05_train_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)


# export_2018-07-06_train

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-06_train/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_export_2018-07-06_train_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/export_2018-07-06_train'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_export_2018-07-06_train_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)


# export_2018-07-07_train

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/export_2018-07-07_train/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_export_2018-07-07_train_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/export_2018-07-07_train'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_export_2018-07-07_train_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)


# intermediate

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/intermediate/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_export_2018-07-08_train_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/intermediate'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_intermediate_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)


# summer_wild_evaluation_dialogs

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/summer_wild_evaluation_dialogs/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_summer_wild_evaluation_dialogs_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/summer_wild_evaluation_dialogs'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_summer_wild_evaluation_dialogs_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)



# tolokers

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/tolokers/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_tolokers_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/tolokers'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_tolokers_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)


# volunteers

json_files = sorted(glob.glob('/home/user1/conversation-data/dataset-01-convai/data/03_filled_data/volunteers/*.json'))

for i, json_file in enumerate(json_files):
    with open(json_file, 'r') as file:
        data = json.load(file)

    filled_data = label_emotion(data)
    print(f"filled_data_volunteers_{i + 1}:", filled_data)
    print("=====================================")

    output_dir = '/home/user1/conversation-data/dataset-01-convai/data/04_emotion_labeled_data/volunteers'
    output_file = os.path.join(output_dir, f'emotion_labeled_data_volunteers_{i + 1}.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filled_data, file, ensure_ascii=False, indent=4)