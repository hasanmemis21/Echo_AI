from transformers import pipeline

classifier = pipeline("text-classification", model="coltekin/berturk-tremo")

def analyze_text_emotion(text):
    try:
        result = classifier(text)
        if result and isinstance(result, list):
            label = result[0]["label"].lower()
            score = round(result[0]["score"], 3)

            # 🔽 Eğer emin değilse, nötr olarak ata
            if score < 0.95:
                return {"label": "nötr", "score": score}
            return {"label": label, "score": score}
        else:
            return {"label": "nötr", "score": 0.0}
    except Exception as e:
        print("Text emotion analysis error:", e)
        return {"label": "error", "score": 0.0}
