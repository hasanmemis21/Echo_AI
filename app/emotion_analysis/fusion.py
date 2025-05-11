from collections import defaultdict

def fuse_emotions(emotions):
    score_table = defaultdict(float)

    for source in emotions.values():
        label = source.get("label")
        score = source.get("score", 0)
        if label not in ["error", "no_face"]:
            score_table[label] += score

    if not score_table:
        return {"label": "nötr", "score": 0.0}

    final_label = max(score_table, key=score_table.get)
    final_score = score_table[final_label]

    return {"label": final_label, "score": round(final_score, 3)}
