# app/emotion_analysis/audio.py

import base64
import logging
import io
from typing import Dict
from transformers import pipeline
from pydub import AudioSegment
import numpy as np

# --- Audio Classification pipeline ---
_audio_classifier = None

def get_audio_classifier():
    global _audio_classifier
    if _audio_classifier is None:
        _audio_classifier = pipeline(
            "audio-classification",
            model="superb/hubert-large-superb-er",
            device=-1
        )
        logging.info("Audio classifier loaded")
    return _audio_classifier


def analyze_audio_emotion_from_base64(b64_string: str, threshold: float = 0.80) -> Dict[str, float]:
    """
    Decode Base64 audio (webm/blob), convert via pydub+ffmpeg to PCM, then classify.
    Returns label and score, 'nötr' if below threshold.
    """
    try:
        # Decode and load with pydub (uses ffmpeg)
        audio_bytes = base64.b64decode(b64_string)
        seg = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
        # Convert to mono numpy array
        samples = np.array(seg.get_array_of_samples())
        if seg.channels > 1:
            samples = samples.reshape((-1, seg.channels)).mean(axis=1).astype(samples.dtype)
        # Run classifier
        classifier = get_audio_classifier()
        result = classifier(samples, sampling_rate=seg.frame_rate)
        label = result[0]["label"].lower()
        score = round(result[0]["score"], 3)
        # Apply user-adjusted threshold
        if score < threshold:
            label = "nötr"
        return {"label": label, "score": score}
    except Exception as e:
        logging.error("Audio emotion error: %s", e)
        return {"label": "error", "score": 0.0}
