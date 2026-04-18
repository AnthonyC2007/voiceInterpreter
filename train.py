import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

LEARNING_RATE = 0.001
BATCH_SIZE = 16
EPOCHS = 10000

classes = {
    "neutral": 0,
    "sad": 1,
    "fear": 2,
    "happy": 3,
    "disgust": 4,
    "angry": 5
}

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.l1 = nn.Linear(3, 32)
        self.act1 = nn.ReLU()
        self.l2 = nn.Linear(32, 16)
        self.drop = nn.Dropout(0.2) # Dropout layer to prevent overfitting(randomly zeroes some of the elements of the input during training)
        self.act2 = nn.ReLU()
        self.l3 = nn.Linear(16, 6)

    def forward(self, x):
        out = self.l1(x)
        out = self.act1(out)
        out = self.l2(out)
        out = self.drop(out)
        out = self.act2(out)
        out = self.l3(out)
        return out

def test_model(model, X_test, Y_test):
    model.eval()
    with torch.no_grad():
        outputs = model(X_test)
        _, predicted = torch.max(outputs.data, 1)
        total = Y_test.size(0)
        correct = (predicted == Y_test).sum().item()
        return correct / total

def normalize_features(df):
    df["mean_pitch"] = df["mean_pitch"]-75
    df["mean_pitch"] = df["mean_pitch"]/425
    return df

if __name__ == "__main__":
    # Load features
    df = pd.read_csv("data/features.csv")
    df = normalize_features(df)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    X_train = train_df[["jitter", "shimmer", "mean_pitch"]].values
    Y_train = train_df["label"].map(classes).values
    X_test = test_df[["jitter", "shimmer", "mean_pitch"]].values
    Y_test = test_df["label"].map(classes).values

    # Convert to tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    Y_train_tensor = torch.tensor(Y_train, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    Y_test_tensor = torch.tensor(Y_test, dtype=torch.long)

    # Create model, loss function, and optimizer
    model = Model()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    epochs_history = []
    loss_history = []
    acc_history = []
    # Training loop
    for epoch in range(EPOCHS):
        outputs = model(X_train_tensor)
        loss = loss_fn(outputs, Y_train_tensor)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if epoch % 100 == 0:
            epochs_history.append(epoch)
            loss_history.append(loss.item())
            accuracy = test_model(model, X_test_tensor, Y_test_tensor)
            acc_history.append(accuracy)
            print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {loss.item():.4f}, Accuracy: {accuracy*100:.2f}%")

    fig, ax = plt.subplots(1, 2, figsize=(10, 8))

    ax[0].plot(epochs_history, loss_history, label="Training Loss")
    ax[0].set_xlabel("Epoch")
    ax[0].set_ylabel("Loss")
    ax[0].set_title("Training Loss Over Epochs")
    ax[0].legend()

    ax[1].plot(epochs_history, acc_history, label="Training Accuracy")
    ax[1].set_xlabel("Epoch")
    ax[1].set_ylabel("Accuracy")
    ax[1].set_title("Training Accuracy Over Epochs")
    ax[1].legend()
    plt.show()