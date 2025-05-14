
# import base64
# import logging
# import io
# from typing import Dict, Union
# from collections import defaultdict

# import numpy as np
# from pydub import AudioSegment
# from pydub.utils import which
# from pydub.silence import detect_nonsilent
# from transformers import pipeline

# # DEBUG logları için temel konfigurasyon
# logging.basicConfig(level=logging.DEBUG)

# # İngilizce etiketleri Türkçeye çevirme haritası
# _LABEL_MAP = {
#     "angry": "öfke",
#     "disgust": "tiksinti",
#     "fearful": "korku",
#     "happy": "mutluluk",
#     "neutral": "nötr",
#     "sad": "üzgün",
#     "surprised": "şaşkınlık"
# }

# _audio_classifier = None

# def get_audio_classifier():
#     """
#     Whisper Large V3 tabanlı, 7 duyguyu destekleyen SER modeli.
#     top_k=5 ile en iyi 5 tahmini döndürür.
#     """
#     global _audio_classifier
#     if _audio_classifier is None:
#         logging.info("Loading SER model: firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3")
#         _audio_classifier = pipeline(
#             "audio-classification",
#             model="firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3",
#             device=-1,
#             top_k=5
#         )
#     return _audio_classifier


# def trim_silence(seg: AudioSegment, min_silence_len: int = 500, silence_thresh_delta: int = 16) -> AudioSegment:
#     """
#     Sessizlikleri keser: seg.dBFS - silence_thresh_delta eşiğinin altındaki sessizlikleri algılar.
#     """
#     thresh = seg.dBFS - silence_thresh_delta
#     nonsil = detect_nonsilent(seg, min_silence_len=min_silence_len, silence_thresh=thresh)
#     if nonsil:
#         start, end = nonsil[0][0], nonsil[-1][1]
#         return seg[start:end]
#     return seg


# def _prepare_segment(seg: AudioSegment) -> np.ndarray:
#     """
#     - Sessiz baş/sonu keser
#     - Ortalama gain normalize eder
#     - Mono ve 16 kHz'e çevirir
#     - NumPy dizisi ve normalizasyon
#     """
#     # 1) Trim silence
#     seg = trim_silence(seg)
#     # 2) Gain normalize (0 dBFS)
#     seg = seg.apply_gain(-seg.dBFS)
#     # 3) Mono ve 16kHz
#     seg = seg.set_channels(1).set_frame_rate(16000)
#     # 4) NumPy array
#     samples = np.array(seg.get_array_of_samples()).astype(np.float32)
#     # 5) Normalize to [-1,1]
#     max_val = np.max(np.abs(samples)) or 1.0
#     return samples / max_val


# def _analyze_samples(samples: np.ndarray) -> Dict[str, float]:
#     """
#     NumPy sample dizisini sınıflandır ve en baskın duyguyu aggregate yöntemiyle seç.
#     """
#     classifier = get_audio_classifier()
#     results = classifier({"array": samples, "sampling_rate": 16000})
#     logging.debug("Raw audio results: %s", results)

#     # Ensemble: skorları topla
#     agg = defaultdict(float)
#     for r in results:
#         lbl = r["label"].lower()
#         agg[lbl] += r["score"]

#     # En yüksek toplam skorlu etiketi seç
#     best_eng = max(agg, key=agg.get)
#     best_score = round(agg[best_eng], 3)
#     best_tur = _LABEL_MAP.get(best_eng, "nötr")
#     return {"label": best_tur, "score": best_score}


# def analyze_audio_emotion_from_base64(
#     b64_string: str
# ) -> Dict[str, float]:
#     """
#     Base64 ile gelen audio'yu çözümler ve duygu analizini döner.
#     """
#     try:
#         logging.debug("FFmpeg yolu (audio.py/base64): %s", which("ffmpeg"))
#         if "," in b64_string:
#             b64_string = b64_string.split(",", 1)[1]
#         raw = base64.b64decode(b64_string)
#         seg = AudioSegment.from_file(io.BytesIO(raw), format="webm")
#         samples = _prepare_segment(seg)
#         return _analyze_samples(samples)
#     except Exception as e:
#         logging.error("Audio emotion error (base64): %s", e)
#         return {"label": "error", "score": 0.0}


# def analyze_audio_emotion_from_bytes(
#     raw_bytes: Union[bytes, bytearray, io.BytesIO]
# ) -> Dict[str, float]:
#     """
#     Ham bytes olarak gelen audio'yu çözümler ve duygu analizini döner.
#     """
#     try:
#         logging.debug("FFmpeg yolu (audio.py/bytes): %s", which("ffmpeg"))
#         buf = io.BytesIO(raw_bytes) if isinstance(raw_bytes, (bytes, bytearray)) else raw_bytes
#         seg = AudioSegment.from_file(buf, format="webm")
#         samples = _prepare_segment(seg)
#         return _analyze_samples(samples)
#     except Exception as e:
#         logging.error("Audio emotion error (bytes): %s", e)
#         return {"label": "error", "score": 0.0}

import base64
import logging
import io
from typing import Dict, Union
from collections import defaultdict

import numpy as np
import librosa
from pydub import AudioSegment
from pydub.utils import which
from pydub.silence import detect_nonsilent
from transformers import pipeline

# DEBUG logları için temel konfigurasyon
logging.basicConfig(level=logging.DEBUG)

# İngilizce etiketleri Türkçeye çevirme haritası
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
    top_k=5 ile en iyi 5 tahmini döndürür.
    """
    global _audio_classifier
    if _audio_classifier is None:
        logging.info("Loading SER model: firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3")
        _audio_classifier = pipeline(
            "audio-classification",
            model="firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3",
            device=-1,
            top_k=5
        )
    return _audio_classifier

def trim_silence(seg: AudioSegment, min_silence_len: int = 500, silence_thresh_delta: int = 16) -> AudioSegment:
    """
    Sessizlikleri keser: seg.dBFS - silence_thresh_delta eşiğinin altındaki sessizlikleri algılar.
    """
    thresh = seg.dBFS - silence_thresh_delta
    nonsil = detect_nonsilent(seg, min_silence_len=min_silence_len, silence_thresh=thresh)
    if nonsil:
        start, end = nonsil[0][0], nonsil[-1][1]
        return seg[start:end]
    return seg

def _prepare_segment(seg: AudioSegment) -> np.ndarray:
    """
    - Sessiz baş/sonu keser
    - Ortalama gain normalize eder
    - Mono ve 16 kHz'e çevirir
    - NumPy dizisi ve normalizasyon
    """
    seg = trim_silence(seg)
    seg = seg.apply_gain(-seg.dBFS)
    seg = seg.set_channels(1).set_frame_rate(16000)
    samples = np.array(seg.get_array_of_samples()).astype(np.float32)
    max_val = np.max(np.abs(samples)) or 1.0
    return samples / max_val

def _analyze_samples(samples: np.ndarray) -> Dict[str, float]:
    """
    NumPy sample dizisini sınıflandır ve en baskın duyguyu aggregate yöntemiyle seç.
    """
    classifier = get_audio_classifier()
    results = classifier({"array": samples, "sampling_rate": 16000})
    logging.debug("Raw audio results: %s", results)

    agg = defaultdict(float)
    for r in results:
        lbl = r["label"].lower()
        agg[lbl] += r["score"]

    best_eng = max(agg, key=agg.get)
    best_score = round(agg[best_eng], 3)
    best_tur = _LABEL_MAP.get(best_eng, "nötr")
    return {"label": best_tur, "score": best_score}

def extract_audio_features(raw_bytes: Union[bytes, bytearray, io.BytesIO]) -> Dict[str, float]:
    """
    Ham audio bytes'ını alır ve aşağıdaki özellikleri çıkarır:
      - RMS Enerji
      - Tempo (BPM)
      - Ortalama Pitch (YIN yöntemi)
    """
    buf = io.BytesIO(raw_bytes) if isinstance(raw_bytes, (bytes, bytearray)) else raw_bytes
    data, sr = librosa.load(buf, sr=16000, mono=True)
    rms = librosa.feature.rms(y=data)
    energy = float(np.mean(rms))
    tempo, _ = librosa.beat.beat_track(y=data, sr=sr)
    tempo = float(tempo)
    pitches = librosa.yin(y=data, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    pitch = float(np.nanmean(pitches))
    return {"energy": energy, "tempo_bpm": tempo, "pitch_hz": pitch}

def analyze_audio_emotion_from_bytes(
    raw_bytes: Union[bytes, bytearray, io.BytesIO]
) -> Dict[str, Union[Dict[str, float], float]]:
    """
    Ham bytes olarak gelen audio'yu çözümler, duygu analizini ve ekstrakte edilmiş özellikleri döner.
    """
    try:
        logging.debug("FFmpeg yolu (audio.py/bytes): %s", which("ffmpeg"))
        buf = io.BytesIO(raw_bytes) if isinstance(raw_bytes, (bytes, bytearray)) else raw_bytes
        seg = AudioSegment.from_file(buf, format="webm")
        samples = _prepare_segment(seg)
        emotion_res = _analyze_samples(samples)
        features = extract_audio_features(raw_bytes)
        return {"emotion": emotion_res, "features": features}
    except Exception as e:
        logging.error("Audio emotion error (bytes): %s", e)
        return {"label": "error", "score": 0.0}

def analyze_audio_emotion_from_base64(
    b64_string: str
) -> Dict[str, Union[Dict[str, float], float]]:
    """
    Base64 ile gelen audio'yu çözümler, duygu analizini ve ekstrakte edilmiş özellikleri döner.
    """
    try:
        logging.debug("FFmpeg yolu (audio.py/base64): %s", which("ffmpeg"))
        if "," in b64_string:
            b64_string = b64_string.split(",", 1)[1]
        raw = base64.b64decode(b64_string)
        seg = AudioSegment.from_file(io.BytesIO(raw), format="webm")
        samples = _prepare_segment(seg)
        emotion_res = _analyze_samples(samples)
        features = extract_audio_features(raw)
        return {"emotion": emotion_res, "features": features}
    except Exception as e:
        logging.error("Audio emotion error (base64): %s", e)
        return {"label": "error", "score": 0.0}
