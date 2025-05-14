# tests/test_text.py

import pytest
from text import analyze_text_emotion, _LABEL_MAP

@pytest.fixture
def sample_sentences():
    # Her duygu için en az iki örnek cümle
    return {
        "happy": [
            "Bugün harika bir gün!",
            "Bu haber beni çok mutlu etti."
        ],
        "sad": [
            "Üzgünüm, beklediğim gibi olmadı.",
            "Bu durum beni gerçekten üzdü."
        ],
        "anger": [
            "Buna asla izin veremem!",
            "Çok sinirliyim şu an."
        ],
        "fear": [
            "Korkuyorum, bu çok tehlikeli.",
            "Endişeliyim, başıma kötü bir şey gelecek."
        ],
        "surprise": [
            "Bu habere inanamadım!",
            "Gerçekten mi, şaşırdım."
        ],
        "disgust": [
            "Bu gerçekten iğrenç!",
            "Tiksindim o kokudan."
        ],
        "neutral": [
            "Hava bugün nasıl?",
            "Sadece bir gün daha geçti."
        ]
    }

def test_text_emotion_accuracy(sample_sentences):
    total = correct = 0

    for label_en, sentences in sample_sentences.items():
        # 'sad' _LABEL_MAP içinde 'sadness' olarak tanımlı
        map_key = "sadness" if label_en == "sad" else label_en

        for sent in sentences:
            total += 1
            result = analyze_text_emotion(sent)
            pred = result.get("label")

            # Eğer pred İngilizce gelmişse Türkçeye çevir
            # (text.py’de sadece Türkçe dönecek ama tedbir amaçlı)
            for eng, tur in _LABEL_MAP.items():
                if pred == eng:
                    pred = tur

            expected = _LABEL_MAP[map_key]  # Örn. _LABEL_MAP["sadness"] → "üzüntü"
            if pred == expected:
                correct += 1

    accuracy = correct / total
    # Gerçek oranı yazdır
    print(f"Doğruluk oranı: %{accuracy * 100:.2f}")
    assert accuracy >= 0.85, (
        f"Model doğruluğu yetersiz: %{accuracy * 100:.1f} < %85"
    )
