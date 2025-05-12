# app/emotion_analysis/face.py

import io
import base64
import logging
from typing import Dict
from PIL import Image
from transformers import pipeline

# Singleton pipeline örneği
_detector = None

# Modelin İngilizce etiketlerini Türkçeye map’leme
_LABEL_MAP = {
    "anger":    "öfke",
    "contempt": "tiksinme",
    "disgust":  "tiksinme",
    "fear":     "korku",
    "happy":    "mutluluk",
    "sad":      "üzüntü",
    "surprise": "şaşkınlık",
    "neutral":  "nötr"
}

def _get_face_classifier():
    global _detector
    if _detector is None:
        # Tek satırda pipeline ile model yükleniyor
        _detector = pipeline(
            "image-classification",
            model="HardlyHumans/Facial-expression-detection",
            device=-1  # CPU’da çalıştırmak için
        )
        logging.info("Face emotion classifier loaded from HuggingFace")
    return _detector

def analyze_face_emotion(base64_image: str) -> Dict[str, float]:
    """
    Base64 olarak gelen JPEG görüntüsünden duygu etiketini ve skorunu döner.
    """
    try:
        # 1) Base64 → PIL Image
        img_data = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(img_data)).convert("RGB")

        # 2) Pipeline ile sınıflandırma
        classifier = _get_face_classifier()
        outputs = classifier(img, top_k=1)  # [{'label':'happy', 'score':0.95}]
        if not outputs:
            return {"label": "no_face", "score": 0.0}

        raw = outputs[0]
        eng_label = raw["label"].lower()
        score = round(raw["score"], 3)

        # 3) Türkçeye çevir
        tur_label = _LABEL_MAP.get(eng_label, "nötr")
        return {"label": tur_label, "score": score}

    except Exception as e:
        logging.error("Face emotion error: %s", e)
        return {"label": "error", "score": 0.0}
