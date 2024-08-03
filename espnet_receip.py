import os
import re

# 预处理数据，生成所需的文件内容
def preprocess_data(file_path):
    text_lines = []
    wav_scp_lines = []
    utt2spk_lines = []
    uttid_counter = 0

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(': ')
            phn_path = parts[0]
            wav_path = phn_path.replace('/Timit/timit/raw/', '/').replace('.PHN', '.WAV')  # Convert PHN path to WAV path
            landmarks = re.sub(r'[0-9]+:', '', parts[1]).replace('+', '').replace('-', '')
            landmarks = ' '.join(landmarks.split())
            
            uttid = f"uttid{uttid_counter:04d}"  # 生成唯一的ID，确保ID不重复
            uttid_counter += 1
            
            text_lines.append(f"{uttid} {landmarks}")
            wav_scp_lines.append(f"{uttid} {wav_path}")
            utt2spk_lines.append(f"{uttid} {uttid}")
    
    return sorted(text_lines), sorted(wav_scp_lines), sorted(utt2spk_lines)

# 写入文件
def write_to_file(file_path, lines):
    with open(file_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')

# 输入文件路径
data_path = '/g/data/wa66/Xiangyu/Landmark_dataset/Ground_truth/test_landmark_time_new.txt'

# 生成文件内容
text_lines, wav_scp_lines, utt2spk_lines = preprocess_data(data_path)

# 写入文件
write_to_file('text', text_lines)
write_to_file('wav.scp', wav_scp_lines)
write_to_file('utt2spk', utt2spk_lines)

print("文件已生成： text, wav.scp, utt2spk")
