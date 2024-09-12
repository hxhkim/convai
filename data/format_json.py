import json
import os

# JSON 파일들이 있는 디렉토리 경로
input_dir_path = '/home/user1/conversation-data/dataset-01-convai/data/'

# 포맷팅된 JSON 파일들을 저장할 디렉토리 경로
output_dir_path = '/home/user1/conversation-data/dataset-01-convai/data/formatted/'

# 디렉토리가 존재하지 않으면 생성
os.makedirs(output_dir_path, exist_ok=True)

# 디렉토리 내의 모든 파일에 대해 포맷팅 진행
for filename in os.listdir(input_dir_path):
    if filename.endswith('.json'):
        # 입력 파일 경로
        input_file_path = os.path.join(input_dir_path, filename)
        
        # 출력 파일 경로
        output_file_path = os.path.join(output_dir_path, f"formatted_{filename}")
        
        # JSON 파일 읽기
        with open(input_file_path, 'r') as file:
            data = json.load(file)
        
        # 포맷팅된 JSON 데이터
        formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
        
        # 포맷팅된 JSON 데이터를 파일에 저장
        with open(output_file_path, 'w') as file:
            file.write(formatted_json)
        
        print(f"Formatted JSON data has been saved to {output_file_path}")