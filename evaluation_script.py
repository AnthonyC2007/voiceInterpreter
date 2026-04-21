# If you want to run this code locally, make sure to install torch, torchaudio and torchcodec according to these instructions:
# https://pytorch.org/get-started/locally/

import librosa
import numpy as np
import torch
import torch.nn as nn
import pythonosc as osc

class Model(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(3, 3), padding=1, dilation=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2))
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1, dilation=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2))
        )

        self.lstm = nn.LSTM(
            input_size=64, 
            hidden_size=128, 
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )

        self.dropout = nn.Dropout(0.3)

        self.fc = nn.Linear(128*2, 6)

    def forward(self, x):
        x = x.unsqueeze(1)  # (B, 1, T, F)

        x = self.conv1(x)
        x = self.conv2(x)

        # Remove the frequency dimension
        x = x.mean(dim=3) # (B, C, T)
        
        x = x.permute(0, 2, 1)  # (B, T, C)

        # LSTM
        x, _ = self.lstm(x)
        x = x[:, -1, :]  # Take the last time step
        x = self.dropout(x)

        x = self.fc(x)  # (B, 6)

        return torch.softmax(x, dim=1)

def extract_log_mel(audio, sr=16000, n_mels=64, hop_length=256, max_len=300):
    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_mels, hop_length=hop_length)
    log_mel = librosa.power_to_db(mel).T
    
    # Fix length to max_len (300 time steps)
    if len(log_mel) < max_len:
        pad = np.zeros((max_len - len(log_mel), log_mel.shape[1]))
        log_mel = np.vstack([log_mel, pad])
    else:
        log_mel = log_mel[:max_len]
    
    return log_mel.astype(np.float32)

if __name__ == "__main__":
    #Configure torch
    if torch.cuda.is_available():
        print("Using CUDA")
        device = torch.device("cuda")
        torch.backends.cudnn.benchmark = True
    elif torch.xpu.is_available():
        print("Using XPU")
        device =  torch.device("xpu")
    else:
        print("Using CPU")
        device = torch.device("cpu")

    model = Model()
    model.load_state_dict(torch.load("data/crnn_66_73.pth", weights_only=True))
    model.to(device)
    model.eval()

    # Set up OSC server
    # We need audio in 16kHz in array form.

    while True:
        audio: np.ndarray = np.ndarray([])  # Replace with actual audio data
        log_mel_tensor = torch.from_numpy(extract_log_mel(audio)).unsqueeze(0).to(device)  # (1, T, F)
        probabilities = model(log_mel_tensor).cpu().detach().numpy()  # (1, 6)
        print(probabilities)

        # Send probabilities to via OSC
