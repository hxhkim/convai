import os
import json
from pathlib import Path

def find_invalid_emotion_files(base_directory):
    """
    Find message files where emotion scores don't sum to 100
    
    Args:
        base_directory (str): Base directory path containing subdirectories with message files
        
    Returns:
        list: List of invalid message filenames
    """
    invalid_files = []
    
    # Get all subdirectories
    for dir_entry in os.scandir(base_directory):
        if dir_entry.is_dir() and dir_entry.name.startswith(f'convai_emotion_labeled_data_{folder_name}_'):
            # Process each message file in the subdirectory
            message_files = Path(dir_entry.path).glob('message_*.json')
            
            for message_file in message_files:
                try:
                    with open(message_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Calculate sum of emotion scores
                    emotion_scores = data['content']['emotion_scores']
                    score_sum = sum(emotion_scores.values())
                    
                    # Check if sum is not 100
                    if abs(score_sum - 100) > 0.0001:  # Using small epsilon for float comparison
                        invalid_files.append(str(message_file))
                        
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error processing {message_file}: {str(e)}")
                    continue
    
    return invalid_files

def normalize_emotion_scores(invalid_files):
    """
    Normalize emotion scores to sum to 100 for each invalid file
    
    Args:
        invalid_files (list): List of file paths to normalize
        
    Returns:
        tuple: (success_count, error_count, error_files)
    """
    success_count = 0
    error_count = 0
    error_files = []
    
    for file_path in invalid_files:
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get emotion scores
            emotion_scores = data['content']['emotion_scores']
            score_sum = sum(emotion_scores.values())
            
            # Skip if sum is already 100
            if abs(score_sum - 100) <= 0.0001:
                continue
                
            # Normalize scores
            if score_sum > 0:  # Prevent division by zero
                normalization_factor = 100 / score_sum
                for emotion in emotion_scores:
                    emotion_scores[emotion] = round(emotion_scores[emotion] * normalization_factor, 1)
                
                # Handle floating point rounding errors to ensure exact 100
                # Adjust the largest score to make total exactly 100
                total = sum(emotion_scores.values())
                if total != 100:
                    diff = 100 - total
                    max_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
                    emotion_scores[max_emotion] = round(emotion_scores[max_emotion] + diff, 1)
            else:
                # If all scores are 0, distribute evenly
                default_value = 100 / len(emotion_scores)
                for emotion in emotion_scores:
                    emotion_scores[emotion] = round(default_value, 1)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            

            success_count += 1
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            error_count += 1
            error_files.append(file_path)
            continue
    
    return success_count, error_count, error_files

if __name__ == "__main__":

    # folder_name = "intermediate"
    # folder_name = "summer_wild_evaluation_dialogs"
    # folder_name = "tolokers"
    # folder_name = "volunteers"

    # folder_name = "export_2018-07-04_train"
    # folder_name = "export_2018-07-05_train"
    # folder_name = "export_2018-07-06_train"
    folder_name = "export_2018-07-07_train"

    base_dir = f"/home/ubuntu/conversation-data/dataset-01-convai/convai/data/05_final_data/{folder_name}"
    print(f"Finding invalid emotion score files in {folder_name}...")
    invalid_files = find_invalid_emotion_files(base_dir)
    print(f"Found {len(invalid_files)} invalid files")
    
    if invalid_files:
        print("\nNormalizing emotion scores...")
        success, errors, error_files = normalize_emotion_scores(invalid_files)
        print(f"\nResults:")
        print(f"Successfully normalized: {success} files")
        print(f"Errors occurred: {errors} files")
        if errors > 0:
            print("Files with errors:")
            for error_file in error_files:
                print(f"- {error_file}")
    else:
        print("No invalid files found. No normalization needed.")