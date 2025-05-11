from fer import FER
import cv2
import numpy as np
import base64
import io
from PIL import Image
import pandas as pd

def analyze_face_emotion(base64_image):
    try:
        # Base64'ü çöz ve OpenCV formatına çevir
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)

        # FER ile analiz
        detector = FER(mtcnn=True)  # yüz algılamada MTCNN kullan
        result = detector.top_emotion(image_np)

        if result is not None:
            label, score = result
            return {"label": label, "score": round(score, 3)}
        else:
            return {"label": "no_face", "score": 0.0}
    except Exception as e:
        print("Face emotion analysis error:", e)
        return {"label": "error", "score": 0.0}
