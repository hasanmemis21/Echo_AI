# app/emotion_analysis/text.py

from transformers import pipeline

# Global cache için classifier
_classifier = None

def _get_text_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model="coltekin/berturk-tremo",
            device=-1  # CPU’da çalıştır
        )
    return _classifier

def analyze_text_emotion(text):
    try:
        classifier = _get_text_classifier()
        result = classifier(text)
        if isinstance(result, list) and result:
            label = result[0]["label"].lower()
            score = round(result[0]["score"], 3)
            # Emin değilsen nötr olarak ata
            if score < 0.95:
                return {"label": "nötr", "score": score}
            return {"label": label, "score": score}
        return {"label": "nötr", "score": 0.0}
    except Exception as e:
        print("Text emotion analysis error:", e)
        return {"label": "error", "score": 0.0}
