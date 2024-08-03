import os
import numpy as np

def extract_relative_path(full_path):
    # Extract the part of the path that starts from 'TIMIT'
    start_index = full_path.find('TIMIT')
    if start_index != -1:
        return full_path[start_index:]
    return full_path

def load_ground_truth(file_path, selected_landmarks):
    landmarks = {}
    with open(file_path, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            file_path, data = line.split(':', 1)
            relative_path = extract_relative_path(file_path.strip())
            file_name = os.path.splitext(relative_path)[0]  # Remove extension
            words = [item.split(':')[1][0] for item in data.strip().split() if ':' in item]
            # Remove '+' and '-' symbols and filter by selected landmarks
            filtered_words = [word.replace('+', '').replace('-', '') for word in words if word.replace('+', '').replace('-', '') in selected_landmarks]
            landmarks[file_name] = filtered_words
    return landmarks

def load_predictions(file_path, selected_landmarks):
    landmarks = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):  # Adjusting the step to 4 lines to skip the empty line
            if i + 2 >= len(lines):
                break
            wav_name_line = lines[i].strip()
            wav_path_line = lines[i + 1].strip()
            labels_line = lines[i + 2].strip()

            if 'WAV Name' not in wav_name_line or 'WAV Path' not in wav_path_line or 'Labels List' not in labels_line:
                continue

            wav_path = wav_path_line.split(':', 1)[1].strip().replace('\\', '/')
            relative_path = extract_relative_path(wav_path)
            file_name = os.path.splitext(relative_path)[0]  # Remove extension

            words = labels_line.split(':', 1)[1].strip().split()
            # Remove '+' and '-' symbols and filter by selected landmarks
            filtered_words = [word.replace('+', '').replace('-', '') for word in words if word.replace('+', '').replace('-', '') in selected_landmarks]
            file_name = file_name[6:]  # Adjust this if necessary based on your specific needs
            landmarks[file_name] = filtered_words
    return landmarks

def compute_wer(gt_words, pred_words):
    d = np.zeros((len(gt_words) + 1, len(pred_words) + 1), dtype=int)
    
    for i in range(len(gt_words) + 1):
        d[i][0] = i
    for j in range(len(pred_words) + 1):
        d[0][j] = j

    for i in range(1, len(gt_words) + 1):
        for j in range(1, len(pred_words) + 1):
            if gt_words[i - 1] == pred_words[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + 1)
    
    return d[len(gt_words)][len(pred_words)] / len(gt_words)

def main():
    gt_file = '/g/data/wa66/Xiangyu/Landmark_dataset/Ground_truth/test_landmark_time_new.txt'
    pred_file = '/g/data/wa66/Xiangyu/Landmark_dataset/speech_marker/test_speechmarker.txt'
    selected_landmarks = ['f', 'b', 'g', 's', 'v']  # Specify the desired landmarks
    
    ground_truth = load_ground_truth(gt_file, selected_landmarks)
    predictions = load_predictions(pred_file, selected_landmarks)
    
    total_wer = 0
    count = 0

    missing_files = []
    
    for file_name in ground_truth:
        if file_name in predictions:
            gt_words = ground_truth[file_name]
            pred_words = predictions[file_name]
            if len(gt_words) == 0 or len(pred_words) == 0:  # Skip if no landmarks match
                continue
            wer = compute_wer(gt_words, pred_words)
            total_wer += wer
            count += 1
            print(f"WER for {file_name}: {wer}")
        else:
            missing_files.append(file_name)
    
    if count > 0:
        print(f'Number of files processed: {count}')
        print(f"Average WER: {total_wer / count}")
    else:
        print("No matching files found between ground truth and predictions with the specified landmarks.")

    if missing_files:
        print(f'Missing prediction files for {len(missing_files)} ground truth files')
        for file in missing_files:
            print(f'Missing: {file}')
    
if __name__ == "__main__":
    main()
