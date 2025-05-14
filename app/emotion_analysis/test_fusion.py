# tests/test_fusion.py

import pytest
from fusion import fuse_emotions

@pytest.mark.parametrize("inputs,expected_label,expected_score", [
    # Tümü aynı duygu: normalize weighted
    (
        {"text":{"label":"mutluluk","score":0.9},
         "audio":{"label":"mutluluk","score":0.7},
         "face":{"label":"mutluluk","score":0.8}},
        "mutluluk",
        pytest.approx((0.9*1.0 + 0.7*0.8 + 0.8*1.2) / (1.0 + 0.8 + 1.2), rel=1e-3)
    ),
    # İki "öfke" bir "üzüntü": choose highest normalized
    (
        {"text":{"label":"öfke","score":0.6},
         "audio":{"label":"üzüntü","score":0.9},
         "face":{"label":"öfke","score":0.4}},
        "üzüntü",
        pytest.approx((0.9*0.8) / 0.8, rel=1e-3)
    ),
    # Yalnızca iki kanal verildiğinde
    (
        {"text":{"label":"nötr","score":0.5},
         "audio":{"label":"nötr","score":0.5}},
        "nötr",
        pytest.approx((0.5*1.0 + 0.5*0.8) / (1.0 + 0.8), rel=1e-3)
    ),
])
def test_fuse_emotions(inputs, expected_label, expected_score):
    out = fuse_emotions(inputs)
    # En yüksek normalize edilmiş skorlu etiketi ve skoru doğrula
    assert out["label"] == expected_label
    assert out["score"] == expected_score
