# tests/test_face.py

import os
import base64
import pytest
from app.emotion_analysis.face import _get_face_classifier, analyze_face_emotion, _LABEL_MAP

def test_get_face_classifier_loads_pipeline():
    """
    Pipeline’ın doğru yüklendiğini kontrol eder.
    """
    clf = _get_face_classifier()
    assert clf is not None, "Face classifier yüklenemedi"

@pytest.fixture
def face_samples_dir():
    """
    Etiketli yüz görüntülerinin bulunduğu klasör.
    Dosya yapısı:
      tests/data/face/
        happy1.jpeg, happy2.jpeg, ...
        sad1.jpeg, sad2.jpeg, ...
        angry1.jpeg, ...
        ...
    """
    return os.path.join(os.path.dirname(__file__), "data", "face")

def test_face_emotion_accuracy(face_samples_dir):
    """
    Tüm örneklerde modelin doğru duyguyu tespit edip
    en az %85 genel doğruluk sağlaması beklenir.
    """
    samples = []
    for fname in os.listdir(face_samples_dir):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        # Dosya adı “labelX.jpeg” ⇒ ingilizce label
        label_en = os.path.splitext(fname)[0].rstrip("0123456789").lower()
        samples.append((label_en, os.path.join(face_samples_dir, fname)))

    total = len(samples)
    assert total > 0, "Yüz test örneği bulunamadı"

    correct = 0
    for label_en, path in samples:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        res = analyze_face_emotion(b64)
        # İngilizce etiketi Türkçeye çevir
        expected_label_tr = _LABEL_MAP.get(label_en)
        # pipeline’ın döndürdüğü etiketi kontrol et
        if res.get("label") == expected_label_tr:
            correct += 1

    accuracy = correct / total
    assert accuracy >= 0.85, (
        f"Model doğruluğu yetersiz: %{accuracy * 100:.1f} < %85"
    )
