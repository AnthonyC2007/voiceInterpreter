import librosa
import numpy as np
import sounddevice as sd
import torch
import torch.nn as nn
from pythonosc import udp_client
import time

OSC_IP = "127.0.0.1"
OSC_PORT = 7777
OSC_ADDR = "/emotion"

SAMPLE_RATE = 16000
DURATION_SEC = 1.5
MODEL_PATH = "data/crnn_68_77.pth"

EMOTIONS = ["neutral", "sad", "fear", "happy", "disgust", "angry"]


class CRNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(3, 3), padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2))
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1),
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
        self.fc = nn.Linear(128 * 2, 6)

    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.mean(dim=3)
        x = x.permute(0, 2, 1)
        x, _ = self.lstm(x)
        x = x[:, -1, :]
        x = self.dropout(x)
        return torch.softmax(self.fc(x), dim=1)


def extract_log_mel(audio, n_mels=64, hop_length=256, max_len=300):
    mel = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=n_mels, hop_length=hop_length)
    log_mel = librosa.power_to_db(mel).T

    if len(log_mel) < max_len:
        pad = np.zeros((max_len - len(log_mel), log_mel.shape[1]))
        log_mel = np.vstack([log_mel, pad])
    else:
        log_mel = log_mel[:max_len]

    return log_mel.astype(np.float32)


def record_chunk():
    audio = sd.rec(
        int(DURATION_SEC * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    return audio.flatten()


def run():
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.xpu.is_available():
        device = torch.device("xpu")
    else:
        device = torch.device("cpu")

    model = CRNN()
    model.load_state_dict(torch.load(MODEL_PATH, weights_only=True, map_location=device))
    model.to(device)
    model.eval()

    client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

    print(f"Model loaded from {MODEL_PATH}")
    print(f"Sending to {OSC_IP}:{OSC_PORT} — configure Wekinator with 6 inputs")
    print(f"Emotions order: {EMOTIONS}")
    print("Press Cmd+C to stop.\n")

    while True:
        audio = record_chunk()

        if np.abs(audio).max() < 0.01:
            print("Silence --> Skipping")
            time.sleep(0.05)
            continue

        log_mel = extract_log_mel(audio)
        tensor = torch.from_numpy(log_mel).unsqueeze(0).to(device)

        with torch.no_grad():
            probs = model(tensor).cpu().numpy()[0].tolist()

        top = EMOTIONS[int(np.argmax(probs))]
        print(f"-> {top:8s}  {[f'{p:.2f}' for p in probs]}")

        client.send_message(OSC_ADDR, probs)
        time.sleep(0.05)


if __name__ == "__main__":
    run()
