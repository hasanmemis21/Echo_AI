# app/emotion_analysis/text.py

import logging
from transformers import pipeline
from typing import Dict, Any

_classifier = None

def _get_text_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline("text-classification", model="coltekin/berturk-tremo", device=-1)
        logging.info("Text classifier loaded")
    return _classifier

def analyze_text_emotion(text: str) -> Dict[str, Any]:
    """
    Metni alıp duygu etiketini döner.
    """
    try:
        classifier = _get_text_classifier()
        result = classifier(text)
        label = result[0]["label"].lower()
        score = round(result[0]["score"], 3)
        return {"label": label if score >= 0.95 else "nötr", "score": score}
    except Exception as e:
        logging.error("Text emotion analysis error: %s", e)
        return {"label": "error", "score": 0.0}
