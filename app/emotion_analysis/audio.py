# emotion_analysis/audio.py

import sounddevice as sd
from scipy.io.wavfile import write
import uuid
import os
from transformers import pipeline

# Hugging Face modelini yükle
audio_classifier = pipeline("audio-classification", model="superb/hubert-large-superb-er")

def record_audio(duration=5, sample_rate=16000):
    """
    Mikrofondan ses kaydı alır ve geçici bir .wav dosyasına kaydeder.
    """
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    file_name = f"temp_audio_{uuid.uuid4().hex}.wav"
    write(file_name, sample_rate, recording)
    return file_name
def analyze_audio_emotion(duration=5):
    """
    Mikrofondan alınan sesi kaydedip duyguyu analiz eder.
    """
    audio_path = record_audio(duration)
    result = audio_classifier(audio_path)
    label = result[0]['label'].lower()
    score = round(result[0]['score'], 3)

    os.remove(audio_path)

    # Emin değilse nötr olarak ata
    if score < 0.90:
        return {"label": "nötr", "score": score}
    return {"label": label, "score": score}
