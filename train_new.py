import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

LEARNING_RATE = 0.001
BATCH_SIZE = 32
EPOCHS = 512

classes = {
    "neutral": 0,
    "sad": 1,
    "fear": 2,
    "happy": 3,
    "disgust": 4,
    "angry": 5
}

class Model(nn.Module):
    def __init__(self, input_size=3):
        super().__init__()
        self.relu = nn.LeakyReLU(0.01)
        self.drop = nn.Dropout(0.2)
        self.bnorm1 = nn.BatchNorm1d(64)
        self.l1 = nn.Linear(input_size, 64)
        self.l2 = nn.Linear(64, 32)
        self.l3 = nn.Linear(32, 6)

    def forward(self, x):
        out = self.l1(x)
        out = self.bnorm1(out)
        out = self.relu(out)
        out = self.l2(out)
        out = self.drop(out)
        out = self.relu(out)
        out = self.l3(out)
        return out
    
    def test(self, dataset):
        self.eval()
        inputs = dataset.tensors[0]
        expected = dataset.tensors[1]
        with torch.no_grad():
            output = self(inputs)
            _, predicted = torch.max(output, 1)
            total = expected.size(0)
            correct = (predicted == expected).sum().item()

        return correct / total

def get_device():
    if torch.cuda.is_available():
        print("Using CUDA")
        return torch.device("cuda")
    elif torch.xpu.is_available():
        print("Using XPU")
        return torch.device("xpu")
    else:
        print("Using CPU")
        return torch.device("cpu")

def load_dataset(features, device):
    df = pd.read_csv("data/features_normalized.csv")
    df = df[features + ["label"]]
    df["label"] = df["label"].map(classes).values
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    X_train = train_df[features].values
    Y_train = train_df["label"].values
    X_test = test_df[features].values
    Y_test = test_df["label"].values

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
    Y_train_tensor = torch.tensor(Y_train, dtype=torch.long).to(device)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
    Y_test_tensor = torch.tensor(Y_test, dtype=torch.long).to(device)

    train_dataset = torch.utils.data.TensorDataset(X_train_tensor, Y_train_tensor)
    test_dataset = torch.utils.data.TensorDataset(X_test_tensor, Y_test_tensor)

    return train_dataset, test_dataset

def train(model, train_dataloader, test_dataset, loss_fn, optimizer, device):
    loss_history = []
    acc_history = []
    epochs_history = []

    last_acc = 0.0

    pbar = tqdm(range(EPOCHS), desc="Training", ncols=100)
    for epoch in pbar:
        model.train()
        epoch_loss = 0.0

        for X_batch, Y_batch in train_dataloader:
            X_batch = X_batch.to(device, non_blocking=True)
            Y_batch = Y_batch.to(device, non_blocking=True)
            outputs = model(X_batch)
            loss = loss_fn(outputs, Y_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.detach()

        if (epoch+1) % 16 == 0:
            accuracy = model.test(test_dataset)
            last_acc = accuracy

            acc_history.append(accuracy)
            loss_history.append(epoch_loss.item() / len(train_dataloader))
            epochs_history.append(epoch + 1)

        postfix = {"Acc": f"{last_acc*100:.2f}%"}
        pbar.set_postfix(postfix)

    return loss_history, acc_history, epochs_history

if __name__ == "__main__":
    #Configure torch
    device = get_device()
    torch.backends.cudnn.benchmark = True

    # Load features
    train_dataset, test_dataset = load_dataset(["pitch_mean", "pitch_std", "intensity_mean", "intensity_std", "f1_mean", "jitter"], device)
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, pin_memory=False)

    # Create model, loss function, and optimizer
    model = Model(input_size=6)
    #model.compile()
    model.to(device)

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-5)

    loss_history, acc_history, epochs_history = train(model, train_dataloader, test_dataset, loss_fn, optimizer, device)

    final_acc = model.test(test_dataset)
    print(f"Final Test Accuracy: {final_acc*100:.2f}%")
    final_train_acc = model.test(train_dataset)
    print(f"Final Train Accuracy: {final_train_acc*100:.2f}%")

    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    ax[0].set_xlabel("Epoch")
    ax[0].plot(epochs_history, loss_history, label="Training Loss")
    ax[0].set_ylabel("Loss")
    ax[0].set_title("Training Loss Over Epochs")
    ax[0].legend()

    ax[1].set_xlabel("Epoch")
    ax[1].plot(epochs_history, acc_history, label="Training Accuracy")
    ax[1].set_ylim(0, max(acc_history) * 1.1)
    ax[1].set_ylabel("Accuracy")
    ax[1].set_title("Training Accuracy Over Epochs")
    ax[1].legend()
    plt.show()