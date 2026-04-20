# If you want to run this code locally, make sure to install torch, torchaudio and torchcodec according to these instructions:
# https://pytorch.org/get-started/locally/
# https://github.com/meta-pytorch/torchcodec?tab=readme-ov-file#installing-torchcodec

import pandas as pd
import numpy as np
from datasets import Audio, load_dataset
import librosa
from multiprocessing import cpu_count
from tqdm import tqdm

SAMPLE_RATE = 16000

def fix_length(x, max_len):
    if len(x) < max_len:
        pad = np.zeros((max_len - len(x), x.shape[1]))
        x = np.vstack([x, pad])
    else:
        x = x[:max_len]
    return x

def extract_features(audio, n_mfcc=13, n_mels=64, hop_length=256, max_len=300):
    mfcc = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=n_mfcc, n_mels=n_mels, hop_length=hop_length)

    delta = librosa.feature.delta(mfcc)

    mfcc = mfcc.T
    delta = delta.T

    mel = librosa.feature.melspectrogram(y=audio, sr=SAMPLE_RATE, n_mels=n_mels, hop_length=hop_length)
    log_mel = librosa.power_to_db(mel).T
    
    mfcc = fix_length(mfcc, max_len)
    delta = fix_length(delta, max_len)
    log_mel = fix_length(log_mel, max_len)

    return {
        "mfcc": mfcc.astype(np.float32),        # (T, 13)
        "delta": delta.astype(np.float32),      # (T, 13)
        "log_mel": log_mel.astype(np.float32)   # (T, 64)
    }

# Audio object is with metadata. We only need the raw audio array.
def extract_raw_audio(sample):
    sample["audio"] = sample["audio"]["array"]
    return sample

if __name__ == "__main__":
    classes = {
    "neutral": 0,
    "sad": 1,
    "fear": 2,
    "happy": 3,
    "disgust": 4,
    "angry": 5
    }
    # Prepare dataset
    dataset = load_dataset("Huan0806/gender_emotion_recognition")
    dataset = dataset["train"].remove_columns(["source"])
    dataset = dataset.cast_column("audio", Audio(sampling_rate = SAMPLE_RATE))
    dataset = dataset.map(extract_raw_audio, num_proc = cpu_count())
    df: pd.DataFrame = dataset.to_pandas()
    df["labels"] = df["labels"].str.replace("female_", "", regex=False).str.replace("male_", "", regex=False)
    df["labels"] = df["labels"].map(classes).values

    # Use multiprocessing to extract features in parallel
    rows = df.to_dict("records")

    mfcc_list = []
    delta_list = []
    log_mel_list = []
    labels_list = []

    for row in tqdm(rows, desc="Extracting features"):
        features = extract_features(row["audio"])

        if features is not None:
            mfcc_list.append(features["mfcc"])
            delta_list.append(features["delta"])
            log_mel_list.append(features["log_mel"])
            labels_list.append(row["labels"])

    mfcc_array = np.stack(mfcc_list)
    delta_array = np.stack(delta_list)
    log_mel_array = np.stack(log_mel_list)
    labels_array = np.array(labels_list)

    np.savez("data/features_mfcc.npz", mfcc=mfcc_array, delta=delta_array, log_mel=log_mel_array, labels=labels_array)
    print("Feature extraction completed and saved to features_mfcc.npz")
