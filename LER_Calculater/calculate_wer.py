import os
import pdb

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
        for line in f:
            if ':' not in line:
                continue
            file_path, data = line.split(':', 1)
            relative_path = extract_relative_path(file_path.strip())
            file_name = os.path.splitext(relative_path)[0]  # Remove extension
            words = [item.split(':')[1][0] for item in data.strip().split() if ':' in item]
            # pdb.set_trace()
            # Remove '+' and '-' symbols and filter by selected landmarks
            filtered_words = [word.replace('+', '').replace('-', '') for word in words if word.replace('+', '').replace('-', '') in selected_landmarks]
            landmarks[file_name] = filtered_words
    return landmarks


def compute_wer(gt_words, pred_words):
    import numpy as np
    
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
    pred_file = '/g/data/wa66/Xiangyu/Landmark_dataset/auto-landmark/basic/test_landmark_time.txt'
    
    selected_landmarks = ['f', 'b', 'g', 's', 'v']  # Specify the desired landmarks 'f', 'b', 'g', 's', 'v'
    
    ground_truth = load_ground_truth(gt_file, selected_landmarks)
    predictions = load_predictions(pred_file, selected_landmarks)
    
    total_wer = 0
    count = 0
    
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
    
    if count > 0:
        print(f'number of file is {count}')
        print(f"Average WER: {total_wer / count}")
    else:
        print("No matching files found between ground truth and predictions with the specified landmarks.")
    
if __name__ == "__main__":
    main()