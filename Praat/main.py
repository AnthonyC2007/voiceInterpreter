import parselmouth
from parselmouth.praat import call
import numpy as np
import sounddevice as sd #tool used to record mic
import soundfile as sf #used for writing audio files
from pythonosc import udp_client
from typing import Optional, Tuple
import tempfile, os, time

OSC_IP = "127.0.0.1"
OSC_PORT = 6448
OSC_ADDR = "/wek/inputs"



client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT) #creates a UDP socket that knows where to send the data

#Recording settings
SAMPLE_RATE = 44100
DURATION_SEC = 1.5
CHANNELS = 1

def record_chunk() -> np.ndarray:
    """Records a short chunk of audio from the microphone"""
    audio = sd.rec(
        int(DURATION_SEC * SAMPLE_RATE), #records 1.5s of mono audio from the microphone at 44100hz
        samplerate = SAMPLE_RATE,
        channels = CHANNELS,
        dtype = "float32"
    )
    sd.wait() #waits until recording is complete before returning the audio array
    return audio

def extract_features(audio: np.ndarray) -> Optional[Tuple[float, float, float]]:
    """This function will write the audio chunk to a temp .wav, run Praat analysis,
    return (jitter_pct, shimmer_pct, mean_pitch_hz). And returns
    None if the audio is too quiet or unvoiced."""

    #Write to a temp file - Parselmouth requires a file path
    with tempfile.NamedTemporaryFile(suffix = ".wav", delete = False) as f: 
        tmp_path = f.name
    sf.write(tmp_path, audio, SAMPLE_RATE) #writes the audio wave into a sound file for Praat to work with

    try:
        sound = parselmouth.Sound(tmp_path)

        pitch = sound.to_pitch(
            time_step = 0.01,
            pitch_floor = 75.0,
            pitch_ceiling = 500.0 #range of human voice (75 - 500 hz) and extracts pitch track
        )

        pitch_values = pitch.selected_array['frequency']
        voiced = pitch_values[pitch_values > 0] 

        if len(voiced) < 5: #skips the chunk if fewer that 5 voiced frames are found
            return None #Wont analyse chunk if there not enough voiced frames
        
        mean_pitch = float(np.mean(voiced)) #calculates the mean voice pitch in Hz across voiced frames

        point_process = call([sound, pitch], "To PointProcess (cc)") #marks each glottal pulse, used to measure timing irregularities

        jitter = call( #calculates jitter (cycle to cycle variation in pitch period length)(roughness/tremors in voice)
            point_process, 
            "Get jitter (local)",
            0.0, 0.0, 0.0001, 0.02, 1.3
        )#0.0 is start and end time 0.0 means to use the whole recording
        #0.0001 minimum period -> shorter cycles are ignored
        #0.02 maximum period -> longer cycles are ignored as it will be less that 50hz, below human voice floor
        #1.3 Maximum period ratio ->if two adjacent cycles differ in length by more the 1.3x, Praat treats it as a skip and excludes it

        shimmer = call(#calculates shimmer (cylce to cylce variation in amplitude)(breathiness/instability)
            [sound, point_process],
            "Get shimmer (local)",
            0.0, 0.0, 0.0001, 0.02, 1.3, 1.6
        )#everything is same except for extra 1.6 which is maximum amplitude ratio -> if adjacent cycles differ by more than 1.6x, the pair is excluded as an outlier

        return (
            round(jitter * 100, 4), #converts into a readable percentage
            round(shimmer * 100, 4),
            round(mean_pitch, 2)
        ) #returns all three features as percentages (jitter/shimmer) and Hz (pitch)
    finally:
        os.unlink(tmp_path) #delete temp file to make space for new one


def send_to_wekinator(jitter: float, shimmer: float, pitch: float):
    """Send a vector with 3 elements to Wekinator via OSC."""
    client.send_message(OSC_ADDR, [jitter, shimmer, pitch])
    print(f"-> OSC sent jitter={jitter:.4f}% shimmer={shimmer:.4f}% pitch={pitch:.1f}Hz")


def run():
    print("Running")
    print(f"Sending to {OSC_IP}:{OSC_PORT}")
    print("Configure Wekinator with 3 inputs")
    print("Press Cmd+C to stop.\n")

    while True: #infinite loop till stopped by user
        audio = record_chunk() #calling the functions
        features = extract_features(audio)

        if features is None:
            print("Silence / Unvoiced --> Skipping")
        else:
            jitter, shimmer, pitch = features
            send_to_wekinator(jitter, shimmer, pitch)
        
        time.sleep(0.05) #avoids congestion


if __name__ == "__main__":
    run()
