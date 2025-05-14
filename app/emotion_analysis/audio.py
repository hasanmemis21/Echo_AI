import base64
import logging
import io
from typing import Dict, Union

import numpy as np
from pydub import AudioSegment
from pydub.utils import which
from transformers import pipeline

# DEBUG logları için temel konfigurasyon
logging.basicConfig(level=logging.DEBUG)

# İngilizce etiketleri Türkçeye çevirme haritası\
_LABEL_MAP = {
    "angry": "öfke",
    "disgust": "tiksinti",
    "fearful": "korku",
    "happy": "mutluluk",
    "neutral": "nötr",
    "sad": "üzgün",
    "surprised": "şaşkınlık"
}

_audio_classifier = None

def get_audio_classifier():
    """
    Whisper Large V3 tabanlı, 7 duyguyu destekleyen SER modeli.
    Top-3 çıktıyı alacak şekilde pipeline oluşturulur.
    """
    global _audio_classifier
    if _audio_classifier is None:
        logging.info("Loading SER model: firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3")
        _audio_classifier = pipeline(
            "audio-classification",
            model="firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3",
            device=-1,
            top_k=3
        )
    return _audio_classifier


def _prepare_segment(seg: AudioSegment) -> np.ndarray:
    """
    Mono'ya indirir, 16 kHz'e resample eder,
    normalize eder ve NumPy dizisi olarak döner.
    """
    seg = seg.set_channels(1).set_frame_rate(16000)
    samples = np.array(seg.get_array_of_samples()).astype(np.float32)
    max_val = np.max(np.abs(samples)) or 1.0
    return samples / max_val


def analyze_audio_emotion_from_base64(
    b64_string: str, threshold: float = 0.0
) -> Dict[str, float]:
    """
    Base64 ile gelen audio'yu çözümler, Whisper SER pipeline'a verir,
    dönen en yüksek puanlı etiketi Türkçeye çevirerek ve skorla birlikte döner.
    """
    try:
        logging.debug("FFmpeg yolu (audio.py): %s", which("ffmpeg"))
        # prefix'i atla
        if "," in b64_string:
            b64_string = b64_string.split(",", 1)[1]

        raw = base64.b64decode(b64_string)
        seg = AudioSegment.from_file(io.BytesIO(raw), format="webm")
        samples = _prepare_segment(seg)

        classifier = get_audio_classifier()
        results = classifier({"array": samples, "sampling_rate": 16000})
        logging.debug("Raw audio results: %s", results)

        top = results[0]
        eng_label = top["label"].lower()
        score = round(top["score"], 3)
        tur_label = _LABEL_MAP.get(eng_label, "nötr")
        return {"label": tur_label, "score": score}

    except Exception as e:
        logging.error("Audio emotion error (base64): %s", e)
        return {"label": "error", "score": 0.0}


def analyze_audio_emotion_from_bytes(
    raw_bytes: Union[bytes, bytearray, io.BytesIO], threshold: float = 0.0
) -> Dict[str, float]:
    """
    Ham bytes (FormData veya dosya read) ile gelen audio'yu çözümler
    ve Whisper SER pipeline ile analiz eder.
    """
    try:
        logging.debug("FFmpeg yolu (bytes): %s", which("ffmpeg"))
        buf = io.BytesIO(raw_bytes) if isinstance(raw_bytes, (bytes, bytearray)) else raw_bytes
        seg = AudioSegment.from_file(buf, format="webm")
        samples = _prepare_segment(seg)

        classifier = get_audio_classifier()
        results = classifier({"array": samples, "sampling_rate": 16000})
        logging.debug("Raw audio results (bytes): %s", results)

        top = results[0]
        eng_label = top["label"].lower()
        score = round(top["score"], 3)
        tur_label = _LABEL_MAP.get(eng_label, "nötr")
        return {"label": tur_label, "score": score}

    except Exception as e:
        logging.error("Audio emotion error (bytes): %s", e)
        return {"label": "error", "score": 0.0}
