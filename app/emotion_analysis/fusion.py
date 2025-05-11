# app/emotion_analysis/fusion.py

from collections import defaultdict
from typing import Dict, Any

def fuse_emotions(emotions: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    """
    Kaynak bazlı skorlara göre ağırlıklı ortalama ya da voting ile final duygu çıkart.
    """
    # Örnek: farklı kaynaklara farklı ağırlıklar
    weights = {"text": 1.0, "face": 1.2, "audio": 0.8}
    score_table = defaultdict(float)
    total_weight = defaultdict(float)

    for src, val in emotions.items():
        label = val.get("label")
        score = val.get("score", 0)
        w = weights.get(src, 1.0)
        if label and label not in ("error", "no_face"):
            score_table[label] += score * w
            total_weight[label] += w

    if not score_table:
        return {"label": "nötr", "score": 0.0}

    # normalize
    normalized = {lbl: score_table[lbl] / total_weight[lbl] for lbl in score_table}
    final_label = max(normalized, key=normalized.get)
    final_score = round(normalized[final_label], 3)
    return {"label": final_label, "score": final_score}
