# If you want to run this code locally, make sure to install torch, torchaudio and torchcodec according to these instructions:
# https://pytorch.org/get-started/locally/
# https://github.com/meta-pytorch/torchcodec?tab=readme-ov-file#installing-torchcodec

import pandas as pd
import numpy as np
from datasets import Audio, load_dataset
import parselmouth
from parselmouth.praat import call

from multiprocessing import Pool, cpu_count
from tqdm import tqdm # For progress bar

SAMPLE_RATE = 48000
OUTPUT_FILE = "data/features.csv"

# Extracts features from audio
def extract_features(audio):
    sound = parselmouth.Sound(audio, sampling_frequency = SAMPLE_RATE)

    pitch = sound.to_pitch(time_step = 0.01, pitch_floor = 75, pitch_ceiling = 500.0)
    pitch_values = pitch.selected_array['frequency']

    voiced = pitch_values[pitch_values > 0]
    if len(voiced) < 5:
        return None
    
    mean_pitch = float(np.mean(pitch_values))

    # point_process = call(sound, "To PointProcess (periodic, praat)", 75, 500)
    point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)

    try:
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer = call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    except:
        return None

    return jitter, shimmer, mean_pitch

# Helper method to process each row of the dataset in parallel
def process_row(data_row):
    audio = data_row["audio"]
    features = extract_features(audio)

    if features is None:
        return None

    return {
        "label": data_row["labels"],
        "jitter": features[0],
        "shimmer": features[1],
        "mean_pitch": features[2]
    }

# Audio object is with metadata. We only need the raw audio array.
def extract_raw_audio(sample):
    sample["audio"] = sample["audio"]["array"]
    return sample

if __name__ == "__main__":
    # Prepare dataset
    dataset = load_dataset("Huan0806/gender_emotion_recognition")
    dataset = dataset["train"].remove_columns(["source"])
    dataset = dataset.cast_column("audio", Audio(sampling_rate = SAMPLE_RATE))
    dataset = dataset.map(extract_raw_audio, num_proc = cpu_count())
    df: pd.DataFrame = dataset.to_pandas()
    df["labels"] = df["labels"].str.replace("female_", "", regex=False).str.replace("male_", "", regex=False)

    # Use multiprocessing to extract features in parallel
    rows = df.to_dict("records")
    results = []

    with Pool(cpu_count()) as pool:
        for res in tqdm(pool.imap_unordered(process_row, rows, chunksize=10), total=len(rows), desc="Extracting features"):
            results.append(res)

    # Filter out any None results (failed extractions) and create a DataFrame
    results = [r for r in results if r is not None]
    results = pd.DataFrame(results)

    print(results.head())
    results.to_csv(OUTPUT_FILE, index = False)
    print(f"Saved features to {OUTPUT_FILE}")