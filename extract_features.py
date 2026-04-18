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
OUTPUT_FILE_NORMALIZED = "data/features_normalized.csv"

# Extracts features from audio
def get_pitch_features(sound):
    pitch = sound.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
    values = pitch.selected_array['frequency']
    voiced = values[values > 0]

    if len(voiced) < 5:
        return None

    return {
        "pitch_mean": float(np.mean(voiced)),
        "pitch_std": float(np.std(voiced)),
        "pitch_min": float(np.min(voiced)),
        "pitch_max": float(np.max(voiced)),
        "pitch_range": float(np.max(voiced) - np.min(voiced))
    }

def get_intensity_features(sound):
    intensity = sound.to_intensity()
    values = intensity.values[0]

    return {
        "intensity_mean": float(np.mean(values)),
        "intensity_std": float(np.std(values))
    }

def get_formant_features(sound):
    formant = sound.to_formant_burg()

    f1 = []
    f2 = []
    f3 = []

    for t in np.arange(0, sound.duration, 0.01):
        f1.append(formant.get_value_at_time(1, t))
        f2.append(formant.get_value_at_time(2, t))
        f3.append(formant.get_value_at_time(3, t))

    return {
        "f1_mean": float(np.nanmean(f1)),
        "f2_mean": float(np.nanmean(f2)),
        "f3_mean": float(np.nanmean(f3))
    }

def get_hnr_features(sound):
    harmonicity = sound.to_harmonicity()
    values = harmonicity.values[0]

    return {
        "hnr_mean": float(np.mean(values))
    }

def get_jitter_shimmer_features(sound):
    # point_process = call(sound, "To PointProcess (periodic, praat)", 75, 500)
    point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)

    try:
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer = call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    except:
        return None

    return {
        "jitter": jitter,
        "shimmer": shimmer
    }

def extract_features(audio):
    sound = parselmouth.Sound(audio, sampling_frequency = SAMPLE_RATE)

    features = {}

    extractors = [
        get_pitch_features,
        get_intensity_features,
        get_formant_features,
        get_hnr_features,
        get_jitter_shimmer_features
    ]

    for extractor in extractors:
        result = extractor(sound)
        if result is None:
            return None
        features.update(result)

    return features

# Helper method to process each row of the dataset in parallel
def process_row(data_row):
    audio = data_row["audio"]
    features = extract_features(audio)

    if features is None:
        return None

    return features | {"label": data_row["labels"]}

# Audio object is with metadata. We only need the raw audio array.
def extract_raw_audio(sample):
    sample["audio"] = sample["audio"]["array"]
    return sample

# Normalizes features
def normalize_features(df):
    df = df.copy()

    # --- oddziel label ---
    labels = df["label"]
    features = df.drop(columns=["label"])

    # --- zakresy fizyczne ---
    RANGES = {
        "pitch": (75, 500),
        "intensity_mean": (30, 100),
        "intensity_std": (0, 30),
        "f1_mean": (200, 1000),
        "f2_mean": (500, 3000),
        "f3_mean": (1500, 5000),
        "hnr_mean": (0, 40),
        "jitter": (1e-5, 0.02),
        "shimmer": (1e-5, 0.1),
    }

    def minmax(series, xmin, xmax):
        x = (series - xmin) / (xmax - xmin)
        return x.clip(0.0, 1.0)

    def log_minmax(series, xmin, xmax):
        series = series.clip(lower=xmin)  # zabezpieczenie przed log(0)
        x = np.log(series)
        xmin = np.log(xmin)
        xmax = np.log(xmax)
        x = (x - xmin) / (xmax - xmin)
        return pd.Series(x, index=series.index).clip(0.0, 1.0)

    # --- Z-score (tylko wybrane cechy) ---
    zscore_features = ["pitch_std", "pitch_range"]

    z_stats = {}
    for col in zscore_features:
        if col in features.columns:
            mean = features[col].mean()
            std = features[col].std() + 1e-8
            z_stats[col] = (mean, std)

    # --- normalizacja ---
    out = features.copy()

    # --- PITCH (range-based) ---
    for col in ["pitch_mean", "pitch_min", "pitch_max"]:
        if col in out.columns:
            out[col] = minmax(out[col], *RANGES["pitch"])

    # --- Z-SCORE ---
    for col, (mean, std) in z_stats.items():
        out[col] = (out[col] - mean) / std

    # --- INTENSITY ---
    if "intensity_mean" in out.columns:
        out["intensity_mean"] = minmax(out["intensity_mean"], *RANGES["intensity_mean"])

    if "intensity_std" in out.columns:
        out["intensity_std"] = minmax(out["intensity_std"], *RANGES["intensity_std"])

    # --- FORMANTY ---
    for col in ["f1_mean", "f2_mean", "f3_mean"]:
        if col in out.columns:
            out[col] = log_minmax(out[col], *RANGES[col])

    # --- HNR ---
    if "hnr_mean" in out.columns:
        out["hnr_mean"] = out["hnr_mean"] #minmax(out["hnr_mean"], *RANGES["hnr_mean"])

    # --- JITTER / SHIMMER ---
    if "jitter" in out.columns:
        out["jitter"] = out["jitter"] #log_minmax(out["jitter"], *RANGES["jitter"])

    if "shimmer" in out.columns:
        out["shimmer"] = out["shimmer"] #log_minmax(out["shimmer"], *RANGES["shimmer"])

    out["label"] = labels

    return out

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
    print(f"Saved features to {OUTPUT_FILE}\n")

    results_normalized = normalize_features(results)
    print(results_normalized.head())
    results_normalized.to_csv(OUTPUT_FILE_NORMALIZED, index = False)
    print(f"Saved normalized features to {OUTPUT_FILE_NORMALIZED}")
    