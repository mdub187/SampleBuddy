# audio_processing.py
import pydub

import soundfile as sf
import librosa

def load_audio(file_path):
    y, sr = librosa.load(file_path)
    return y, sr

def change_tempo(y, tempo_factor):
    return librosa.effects.time_stretch(y, tempo_factor)

def export_audio(output_file, y, sr):
    sf.write(output_file, y, sr)
