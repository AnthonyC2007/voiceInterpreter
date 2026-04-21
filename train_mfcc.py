import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

LEARNING_RATE = 0.001
WEIGHT_DECAY = 1e-4
BATCH_SIZE = 32
EPOCHS = 50

# B - Batch size
# T - Time steps (300)
# F - Frequency bins (64)
# C - Channels (1 for log-mel, 2 for log-mel + mfcc)

# Best results I've got
# BATCH_SIZE = 32
# EPOCHS = 50
# CRNN model

class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.name = "CNN"

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

        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=(3, 3), padding=1, dilation=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2))
        )

        self.pool = nn.AdaptiveAvgPool2d((1, 1))

        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 6)
        )

    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension

        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)

        x = self.pool(x)
        x = x.flatten(1)  # Flatten all dimensions except batch

        return self.fc(x)
    
    def test(self, dataset, device):
        self.eval()

        correct = 0
        total = 0

        with torch.no_grad():
            for X, Y in dataset:
                X = X.to(device, non_blocking=True)
                Y = Y.to(device, non_blocking=True)

                output = self(X.unsqueeze(0))  # Add batch and channel dimensions
                pred = torch.argmax(output, dim=1)

                correct += (pred.item() == Y.item())
                total += 1

        return correct / total
    
class MinimalCNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.name = "MinimalCNN"

        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1, dilation=1),
            nn.BatchNorm2d(16),
            nn.ReLU()
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=(3, 3), padding=1, dilation=1),
            nn.BatchNorm2d(32),
            nn.ReLU()
        )

        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(32, 6)

    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension

        x = self.conv1(x)
        x = self.conv2(x)

        x = self.pool(x)
        x = x.view(x.size(0), -1)  # Flatten

        return self.fc(x)
    
    def test(self, dataset, device):
        self.eval()

        correct = 0
        total = 0

        with torch.no_grad():
            for X, Y in dataset:
                X = X.to(device, non_blocking=True)
                Y = Y.to(device, non_blocking=True)

                output = self(X.unsqueeze(0))  # Add batch and channel dimensions
                pred = torch.argmax(output, dim=1)

                correct += (pred.item() == Y.item())
                total += 1

        return correct / total

class SimpleCRNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.name = "SimpleCRNN"

        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(3, 3), padding=1, dilation=1),
            nn.BatchNorm2d(32),
            nn.ReLU()
        )

        self.lstm = nn.LSTM(32, 64, batch_first=True)

        self.fc = nn.Linear(64, 6)

    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension

        x = self.conv(x)
        x = x.mean(dim=3)  # Remove the frequency dimension

        x = x.permute(0, 2, 1)  # (B, T, C)
        x, _ = self.lstm(x)
        x = x[:, -1, :]  # Take the last time step

        return self.fc(x)
    
    def test(self, dataset, device):
        self.eval()

        correct = 0
        total = 0

        with torch.no_grad():
            for X, Y in dataset:
                X = X.to(device, non_blocking=True)
                Y = Y.to(device, non_blocking=True)

                output = self(X.unsqueeze(0))  # Add batch and channel dimensions
                pred = torch.argmax(output, dim=1)

                correct += (pred.item() == Y.item())
                total += 1

        return correct / total

class CRNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.name = "CRNN"

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

        return self.fc(x)
    
    def test(self, dataset, device):
        self.eval()

        correct = 0
        total = 0

        with torch.no_grad():
            for X, Y in dataset:
                X = X.to(device, non_blocking=True)
                Y = Y.to(device, non_blocking=True)

                output = self(X.unsqueeze(0))  # Add batch and channel dimensions
                pred = torch.argmax(output, dim=1)

                correct += (pred.item() == Y.item())
                total += 1

        return correct / total

class EmotionDataset(Dataset):
    def __init__(self, log_mel, labels):
        self.X = log_mel
        self.Y = labels

    def __len__(self):
        return len(self.Y)

    def __getitem__(self, idx):
        x = self.X[idx]  # (T, F)
        y = self.Y[idx]

        return (torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.long))

def load_dataset():
    data = np.load("data/features_log_mel.npz")
    
    log_mel = data["log_mel"]  # (N, T, 64)
    labels = data["labels"]  # (N,)

    X_train, X_test, Y_train, Y_test = train_test_split(log_mel, labels, test_size=0.2, random_state=42)

    train_dataset = EmotionDataset(X_train, Y_train)
    test_dataset = EmotionDataset(X_test, Y_test)

    return train_dataset, test_dataset

def train(model, train_dataloader, test_dataset, loss_fn, optimizer, device):
    loss_history = []
    accuracy_history = []

    pbar = tqdm(range(EPOCHS), desc=f"Training {model.name}", ncols=100)
    for epoch in pbar:
        model.train()
        epoch_loss = 0.0

        for X_batch, Y_batch in train_dataloader:
            X_batch = X_batch.to(device, non_blocking=True)
            Y_batch = Y_batch.to(device, non_blocking=True)

            outputs = model(X_batch)  # Add channel dimension
            loss = loss_fn(outputs, Y_batch)

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.detach()

        loss_history.append(epoch_loss.item()/BATCH_SIZE) # type: ignore
        accuracy_history.append(model.test(test_dataset, device))

    return loss_history, accuracy_history

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

    #Load dataset
    train_dataset, test_dataset = load_dataset()
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)

    #Initialize model, loss function and optimizer
    model = CNN()
    model = model.to(device)
    print(f"Initial Test Accuracy: {model.test(test_dataset, device)*100:.2f}%")  # Warm up the model

    loss_fn = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    #Train and test
    loss_hist, accuracy_hist = train(model, train_loader, test_dataset, loss_fn, optimizer, device)

    print(f"Final Test Accuracy: {model.test(test_dataset, device)*100:.2f}%")
    print(f"Final Train Accuracy: {model.test(train_dataset, device)*100:.2f}%")

    #Nice plot
    fig, ax = plt.subplots(1, 2, figsize=(10, 8))
    ax[0].set_xlabel("Epoch")
    ax[0].plot(range(len(loss_hist)), loss_hist, label="Training Loss")
    ax[0].set_ylim(0, max(loss_hist)*1.2)
    ax[0].set_ylabel("Loss")
    ax[0].set_title("Training Loss Over Epochs")
    ax[0].grid()
    ax[0].legend()

    ax[1].set_xlabel("Epoch")
    ax[1].plot(range(len(accuracy_hist)), accuracy_hist, label="Test Accuracy")
    ax[1].set_ylim(0, 1)
    ax[1].set_ylabel("Accuracy")
    ax[1].set_title("Test Accuracy Over Epochs")
    ax[1].grid()
    ax[1].legend()

    plt.show()