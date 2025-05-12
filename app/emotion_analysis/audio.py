# app/emotion_analysis/audio.py

from transformers import pipeline
import logging

# Global cache
_asr_pipeline = None

def get_asr_pipeline():
    global _asr_pipeline
    if _asr_pipeline is None:
        # wav2vec2 veya tercih ettiğin başka bir model
        _asr_pipeline = pipeline(
            "automatic-speech-recognition",
            model="facebook/wav2vec2-large-xlsr-53",
            device=-1
        )
        logging.info("ASR pipeline yüklendi")
    return _asr_pipeline

def transcribe_audio(data_bytes: bytes) -> str:
    """
    Byte olarak gelen wav/webm verisini metne çevirir.
    """
    try:
        asr = get_asr_pipeline()
        result = asr(data_bytes)
        return result.get("text", "")
    except Exception as e:
        logging.error("ASR hatası: %s", e)
        return ""
