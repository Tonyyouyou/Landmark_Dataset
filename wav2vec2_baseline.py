import os
import re
import torchaudio
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import Wav2Vec2Model
from jiwer import wer
import pdb
# 检查CUDA是否可用
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Step 1: Preprocess the Data
def preprocess_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(': ')
            phn_path = parts[0]
            wav_path = phn_path.replace('/Timit/timit/raw/', '/').replace('.PHN', '.WAV')  # Convert PHN path to WAV path
            landmarks = re.sub(r'[0-9]+:', '', parts[1]).replace('+', '').replace('-', '')
            landmarks = landmarks.split()
            data.append((wav_path, landmarks))
    return data

# Step 2: Create a Dataset Class
class LandmarkDataset(Dataset):
    def __init__(self, data):
        self.data = data
        self.landmark_to_index = self.build_vocab()
        self.index_to_landmark = {v: k for k, v in self.landmark_to_index.items()}
    
    def build_vocab(self):
        unique_landmarks = set()
        for _, landmarks in self.data:
            unique_landmarks.update(landmarks)
        return {landmark: idx for idx, landmark in enumerate(unique_landmarks)}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        path, landmarks = self.data[idx]
        waveform, sample_rate = torchaudio.load(path)
        # Resample to 16000 Hz if needed
        if sample_rate != 16000:
            waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(waveform)
        landmarks_tensor = torch.tensor([self.landmark_to_index[lm] for lm in landmarks], dtype=torch.long)
        return waveform.squeeze(0), landmarks_tensor

# Custom collate function to pad sequences
def collate_fn(batch):
    waveforms, landmarks = zip(*batch)
    max_length = max(waveform.size(0) for waveform in waveforms)
    
    padded_waveforms = torch.zeros(len(waveforms), max_length)
    for i, waveform in enumerate(waveforms):
        padded_waveforms[i, :waveform.size(0)] = waveform
    
    max_landmarks_length = max(len(lm) for lm in landmarks)
    padded_landmarks = torch.full((len(landmarks), max_landmarks_length), fill_value=-100, dtype=torch.long)  # Use -100 as padding value
    for i, lm in enumerate(landmarks):
        padded_landmarks[i, :len(lm)] = lm
    
    return padded_waveforms, padded_landmarks

# Step 3: Define the Model
class LandmarkDetectionModel(nn.Module):
    def __init__(self, wav2vec_model_name, output_dim, hidden_dim, n_layers, n_heads):
        super(LandmarkDetectionModel, self).__init__()
        self.wav2vec = Wav2Vec2Model.from_pretrained(wav2vec_model_name)
        for param in self.wav2vec.parameters():
            param.requires_grad = False
        
        self.attention = nn.MultiheadAttention(embed_dim=self.wav2vec.config.hidden_size, num_heads=n_heads)
        self.decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=self.wav2vec.config.hidden_size, nhead=n_heads),
            num_layers=n_layers
        )
        self.fc = nn.Linear(self.wav2vec.config.hidden_size, output_dim)
    
    def forward(self, input_audio):
        with torch.no_grad():
            wav2vec_outputs = self.wav2vec(input_audio).last_hidden_state
        
        attn_output, _ = self.attention(wav2vec_outputs, wav2vec_outputs, wav2vec_outputs)
        decoder_output = self.decoder(attn_output, attn_output)
        output = self.fc(decoder_output)
        
        return output

# Step 4: Create the Training and Validation Pipeline
def train_model(data_path, wav2vec_model_name, output_dim, hidden_dim, n_layers, n_heads, num_epochs, batch_size, val_split=0.1):
    data = preprocess_data(data_path)
    dataset = LandmarkDataset(data)
    val_size = int(len(dataset) * val_split)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)

    model = LandmarkDetectionModel(wav2vec_model_name, output_dim, hidden_dim, n_layers, n_heads).to(device)
    criterion = nn.CrossEntropyLoss(ignore_index=-100)  # Ignore padding index
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        for batch in train_loader:
            audio, landmarks = batch
            audio = audio.to(device)
            landmarks = landmarks.to(device)
            optimizer.zero_grad()
            outputs = model(audio)
            
            # Ensure outputs and landmarks have matching shapes
            batch_size, seq_len, _ = outputs.shape
            pdb.set_trace()
            outputs = outputs[:, :landmarks.size(1), :].contiguous()
            outputs = outputs.view(-1, output_dim)
            landmarks = landmarks.view(-1)
            
            loss = criterion(outputs, landmarks)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        # print(f'the training loss is {train_loss}')

        model.eval()
        val_loss = 0.0
        val_wer = 0.0
        with torch.no_grad():
            for batch in val_loader:
                audio, landmarks = batch
                audio = audio.to(device)
                landmarks = landmarks.to(device)
                outputs = model(audio)
                
                # Ensure outputs and landmarks have matching shapes
                batch_size, seq_len, _ = outputs.shape
                outputs = outputs[:, :landmarks.size(1), :].contiguous()
                outputs = outputs.view(-1, output_dim)
                landmarks = landmarks.view(-1)
                
                loss = criterion(outputs, landmarks)
                val_loss += loss.item()
                
                # Calculate WER
                pred = outputs.argmax(dim=-1).cpu().numpy()
                truth = landmarks.cpu().numpy()
                pred_str = ' '.join([dataset.index_to_landmark[i] for i in pred if i != -100])
                truth_str = ' '.join([dataset.index_to_landmark[i] for i in truth if i != -100])
                val_wer += wer(truth_str, pred_str)

        val_loss /= len(val_loader)
        val_wer /= len(val_loader)
        
        print(f'Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss}, Val Loss: {val_loss}, Val WER: {val_wer}')

# Example usage
data_path = '/g/data/wa66/Xiangyu/Landmark_dataset/Ground_truth/train_landmark_time_new.txt'
wav2vec_model_name = 'facebook/wav2vec2-large-960h'
output_dim = 5  # Adjust according to the number of unique landmarks
hidden_dim = 256
n_layers = 3
n_heads = 8
num_epochs = 10
batch_size = 1

train_model(data_path, wav2vec_model_name, output_dim, hidden_dim, n_layers, n_heads, num_epochs, batch_size)
