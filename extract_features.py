import pandas as pd
import numpy as np
from datasets import Audio, load_dataset
import parselmouth
from parselmouth.praat import call

SAMPLE_RATE = 48000

# Cleans male_ and female_ prefixes from labels
def clean_prefix(batch):
    return {
        key: [v.replace("female_", "").replace("male_", "") if isinstance(v, str) else v for v in values]
        for key, values in batch.items()
    }

# Extracts features from audio
def extract_features(audio):
    sound = parselmouth.Sound(audio, sampling_frequency = SAMPLE_RATE)

    pitch = sound.to_pitch(time_step = 0.01, pitch_floor = 75, pitch_ceiling = 500.0)
    pitch_values = pitch.selected_array['frequency']

    voiced = pitch_values[pitch_values > 0]
    if len(voiced) < 5:
        return None
    
    mean_pitch = float(np.mean(pitch_values))

    # try:
    #     point_process = call(sound, "To PointProcess (periodic, praat)", 75, 500)
    # except:
    #     point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)
    point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)

    try:
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer = call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    except:
        return None

    return jitter, shimmer, mean_pitch

if __name__ == "__main__":
    # Prepare dataset
    ds = load_dataset("Huan0806/gender_emotion_recognition")
    ds = ds["train"].remove_columns(["source"])
    ds = ds.map(clean_prefix, batched = True)
    ds = ds.cast_column("audio", Audio(sampling_rate = SAMPLE_RATE))

    rows = []
    progress = 0
    length = len(ds)

    for data_row in ds:
        audio = data_row["audio"]["array"]
        features = extract_features(audio)

        if features is None:
            continue

        rows.append({
            "label": data_row["labels"],
            "jitter": features[0],
            "shimmer": features[1],
            "mean_pitch": features[2]
        })

        progress += 1
        print(f"Progress: {progress}/{length}", end = "\r")

    df = pd.DataFrame(rows)
    print(df.head())
    df.to_csv("data/features.csv", index = False)