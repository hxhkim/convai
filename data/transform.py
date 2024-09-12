import json  # JSON 데이터를 다루기 위한 json 모듈을 임포트

# 파일 읽기
with open('/home/user1/conversation-data/dataset-01-convai/data/formatted/formatted_data_intermediate.json', 'r') as file:
    data = json.load(file)  # JSON 파일을 읽어서 data 변수에 저장

# data가 리스트인지 확인하고 첫 번째 요소를 사용
if isinstance(data, list):  # data가 리스트인지 확인
    data = data[0]  # 리스트인 경우 첫 번째 요소를 사용

# 변환 작업
transformed_data = {
    "dialogs": [],  # 변환된 대화 데이터를 저장할 리스트
    "assistant": {
        "personality": data.get("bot_profile", [])  # bot_profile을 assistant의 personality에 저장
    },
    "user": {
        "personality": data.get("user_profile", [])  # user_profile을 user의 personality에 저장
    }
}

# 첫 5개의 대화만 변환
for dialog in data.get("dialogs", [])[:5]:  # 첫 5개의 대화만 순회
    transformed_dialog = {
        "utterance_id": dialog.get("id"),  # id를 utterance_id로 설정
        "utterer": dialog.get("sender"),  # sender를 utterer로 설정
        "text": dialog.get("text"),  # text를 text로 설정
        "role": "assistant" if dialog.get("sender_class") == "Bot" else "user"  # sender_class를 role로 설정, Bot은 assistant로, Human은 user로 변경
    }
    transformed_data["dialogs"].append(transformed_dialog)  # 변환된 대화를 dialogs 리스트에 추가

# 파일 쓰기
with open('transformed_formatted_summer_wild_evaluation_dialogs_test.json', 'w') as f:
    json.dump(transformed_data, f, indent=4)  # 변환된 데이터를 JSON 파일로 저장, 들여쓰기는 4칸









# import json

# # 파일 읽기
# with open('/home/user1/conversation-data/dataset-01-convai/data/formatted/formatted_data_intermediate.json', 'r') as f:
#     data = json.load(f)

# # 변환 작업
# transformed_data = {
#     "dialogs": [],
#     "assistant": {
#         "personality": data.get("bot_profile", [])
#     },
#     "user": {
#         "personality": data.get("user_profile", [])
#     }
# }

# for dialog in data.get("dialogs", []):
#     transformed_dialog = {
#         "utterance_id": dialog.get("id"),
#         "utterer": dialog.get("sender"),
#         "text": dialog.get("text"),
#         "role": "assistant" if dialog.get("sender_class") == "Bot" else "user"
#     }
#     transformed_data["dialogs"].append(transformed_dialog)

# # 파일 쓰기
# with open('transformed_formatted_summer_wild_evaluation_dialogs.json', 'w') as f:
#     json.dump(transformed_data, f, indent=4)