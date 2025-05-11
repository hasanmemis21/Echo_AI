# app/emotion_analysis/face.py

import io, logging
import numpy as np
from fer import FER
from typing import Dict
from PIL import Image
import base64
# global cache
_detector = None

def _get_face_detector():
    global _detector
    if _detector is None:
        _detector = FER(mtcnn=True)
        logging.info("Face detector initialized")
    return _detector

def analyze_face_emotion(base64_image: str) -> Dict[str, float]:
    """
    Base64 string -> duygu dön
    """
    try:
        img = Image.open(io.BytesIO(base64.b64decode(base64_image))).convert("RGB")
        image_np = np.array(img)
        detector = _get_face_detector()
        result = detector.top_emotion(image_np)
        if result:
            label, score = result
            return {"label": label, "score": round(score, 3)}
        else:
            return {"label": "no_face", "score": 0.0}
    except Exception as e:
        logging.error("Face emotion error: %s", e)
        return {"label": "error", "score": 0.0}
