# app/emotion_analysis/text.py

import re
import logging
from transformers import pipeline
from typing import Dict, Any

# Global cache for the classifier
_classifier = None

# Patterns to catch explicitly negative/illness keywords
_NEGATIVE_PATTERNS = [
    r"\bhastay[ıiu]\b",
    r"\büzgün(üm)?\b",
    r"\bmutsuz(um)?\b",
    r"\bağlıyorum\b",
    # gerektiğinde buraya ekleyin...
]

# İngilizce → Türkçe etiket eşlemesi
_LABEL_MAP = {
    "happy":    "mutluluk",
    "sadness":  "üzüntü",
    "anger":    "öfke",
    "fear":     "korku",
    "surprise": "şaşkınlık",
    "love":     "sevgi",
    "neutral":  "nötr",
    "disgust":  "tiksinme",
}

def _get_text_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model="coltekin/berturk-tremo",
            device=-1
        )
        logging.info("Text classifier loaded")
    return _classifier

def analyze_text_emotion(text: str) -> Dict[str, Any]:
    """
    Metni alıp duygu etiketini Türkçe olarak döner.
    Olumsuz anahtar kelime bulunursa doğrudan 'üzüntü' etiketi döner.
    """
    lower = text.lower()

    # 1) Belirlenen negatif kalıplardan biri varsa doğrudan 'üzüntü'
    for pattern in _NEGATIVE_PATTERNS:
        if re.search(pattern, lower):
            return {"label": "üzüntü", "score": 1.0}

    # 2) Aksi halde pipeline ile tahmin et
    try:
        classifier = _get_text_classifier()
        result = classifier(text)
        if isinstance(result, list) and result:
            raw_label = result[0]["label"].lower()
            score = round(result[0]["score"], 3)

            # 3) Eşik değer altındaysa nötr döndür
            if score < 0.6:
                return {"label": "nötr", "score": score}

            # 4) İngilizce etiketi Türkçeye çevir
            turkish_label = _LABEL_MAP.get(raw_label, raw_label)
            return {"label": turkish_label, "score": score}

        # Fallback
        return {"label": "nötr", "score": 0.0}

    except Exception as e:
        logging.error("Text emotion analysis error: %s", e)
        return {"label": "error", "score": 0.0}
