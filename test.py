# from Landmarks_func import extract_all_landmarks

# # file_path = '/g/data/wa66/Xiangyu/Data/TIMIT/TEST/DR1/FAKS0/SA1.WAV'
# # landmarks = extract_all_landmarks(file_path)
# # print(landmarks)

# # import soundfile as sf
# # import os

# # def convert_wav_to_flac(directory):
# #     for root, dirs, files in os.walk(directory):
# #         for filename in files:
# #             if filename.endswith(".WAV"):
# #                 wav_path = os.path.join(root, filename)
# #                 flac_path = wav_path.replace(".WAV", ".flac")
                
# #                 # 读取WAV文件
# #                 data, samplerate = sf.read(wav_path)
# #                 # 将数据写入FLAC文件
# #                 sf.write(flac_path, data, samplerate)

# # # 替换下面的路径为你的音频文件所在的顶级目录
# # top_level_directory = "/g/data/wa66/Xiangyu/Data/TIMIT/TEST"
# # convert_wav_to_flac(top_level_directory)

# # import soundfile as sf
# # import os

# # def convert_to_standard_wav(directory):
# #     for root, dirs, files in os.walk(directory):
# #         for filename in files:
# #             if filename.lower().endswith(".wav"):
# #                 wav_path = os.path.join(root, filename)
# #                 try:
# #                     # 读取WAV文件
# #                     data, samplerate = sf.read(wav_path)
# #                     # 用标准WAV格式重新写入文件
# #                     sf.write(wav_path, data, samplerate, format='WAV', subtype='PCM_16')
# #                 except Exception as e:
# #                     print(f"Error converting {wav_path}: {e}")

# # # 替换下面的路径为你的音频文件所在的顶级目录
# # top_level_directory = "/g/data/wa66/Xiangyu/Data/TIMIT/TEST"
# # convert_to_standard_wav(top_level_directory)


# import os
# import numpy as np

# # # 假设这是您提到的函数。您需要用实际的函数实现替换它。
# # def extract_all_landmarks(audio_file_path):
# #     # 这里应该是提取landmarks的实际代码
# #     pass

# def merge_and_sort_landmarks(landmarks):
#     # 创建一个包含所有landmarks及其时间和标签的列表
#     labeled_landmarks = []
#     for label, points in landmarks.items():
#         for point in points:
#             labeled_landmarks.append((point, label))

#     # 按时间点排序
#     labeled_landmarks.sort(key=lambda x: x[0])
#     # 提取排序后的标签
#     sorted_labels = [label for _, label in labeled_landmarks]
#     return sorted_labels

# def process_audio_files(directory, output_file):
#     with open(output_file, 'w') as f_out:
#         for root, dirs, files in os.walk(directory):
#             for filename in files:
#                 if filename.lower().endswith(".wav"):
#                     file_path = os.path.join(root, filename)
#                     landmarks = extract_all_landmarks(file_path)
#                     sorted_labels = merge_and_sort_landmarks(landmarks)
#                     # 将landmarks转换为字符串格式
#                     landmarks_str = ', '.join(sorted_labels)
#                     f_out.write(f"{file_path}: {landmarks_str}\n")

# # 替换下面的路径为你的音频文件所在的顶级目录和输出文件的路径
# top_level_directory = "/g/data/wa66/Xiangyu/Data/TIMIT/TEST"
# output_file = "/home/561/xz4320/Auto-Landmark/methods/Basic/output.txt"
# process_audio_files(top_level_directory, output_file)
from datasets import load_dataset, load_metric, Dataset, DatasetDict
wer_metric = load_metric("wer")
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Trainer, TrainingArguments

model_name = 'facebook/wav2vec2-large-960h'
processor = Wav2Vec2Processor.from_pretrained(model_name)

model = Wav2Vec2ForCTC.from_pretrained(
    model_name,
    ctc_loss_reduction="mean",
    pad_token_id=processor.tokenizer.pad_token_id,
    vocab_size=len(processor.tokenizer)
)