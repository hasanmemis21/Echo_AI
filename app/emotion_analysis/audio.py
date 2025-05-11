# app/emotion_analysis/audio.py

import io, uuid, logging
from typing import Dict
import sounddevice as sd
from scipy.io.wavfile import write
from transformers import pipeline

# global cache
_audio_classifier = None

def _get_audio_classifier():
    global _audio_classifier
    if _audio_classifier is None:
        _audio_classifier = pipeline(
            "audio-classification",
            model="superb/hubert-large-superb-er",
            device=-1
        )
        logging.info("Audio classifier loaded")
    return _audio_classifier

def record_audio(duration: float = 5.0, sample_rate: int = 16000) -> bytes:
    """
    Mikrofon kaydını ham bytes olarak döner, disk I/O olmaz.
    """
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    # WAV header + veri
    bio = io.BytesIO()
    write(bio, sample_rate, recording)
    return bio.getvalue()

def analyze_audio_emotion(duration: float = 5.0) -> Dict[str, float]:
    """
    Ham bytes üzerinden duygu analizi.
    """
    try:
        data = record_audio(duration)
        # pipeline, buffer desteği isterse: bir temp file yaratmak yerine:
        classifier = _get_audio_classifier()
        result = classifier(data)
        label = result[0]["label"].lower()
        score = round(result[0]["score"], 3)
        if score < 0.90:
            label = "nötr"
        return {"label": label, "score": score}
    except Exception as e:
        logging.error("Audio emotion error: %s", e)
        return {"label": "error", "score": 0.0}
