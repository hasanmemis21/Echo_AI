# app/routes.py

from flask import Blueprint, request, jsonify
from .db import mongo

api_bp = Blueprint("api", __name__)

@api_bp.route("/analyze", methods=["POST"])
def analyze_emotions():
    # Ağır ML kodlarını fonksiyon içinde lazy-load
    from .emotion_analysis.text import analyze_text_emotion
    from .emotion_analysis.face import analyze_face_emotion
    from .emotion_analysis.audio import analyze_audio_emotion
    from .emotion_analysis.fusion import fuse_emotions
    from .music_recommender import recommend_music

    data = request.json or {}
    text      = data.get("text")
    face_data = data.get("face")
    use_audio = data.get("use_audio", False)

    results = {}
    if text:
        results["text"] = analyze_text_emotion(text)
    if face_data:
        results["face"] = analyze_face_emotion(face_data)
    if use_audio:
        results["audio"] = analyze_audio_emotion()

    if not results:
        return jsonify({"error": "Hiçbir analiz yapılamadı."}), 400

    fused      = fuse_emotions(results)
    music_list = recommend_music(fused)

    mongo.db.logs.insert_one({
        "input": data,
        "results": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    })

    return jsonify({
        "emotions": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    })
