"""# app/routes.py

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin     # ← CORS izni için
from .db import mongo

api_bp = Blueprint("api", __name__)

@api_bp.route("/analyze", methods=["POST"])
@cross_origin(origins="*")               # ← Tüm origin’lere izin ver
def analyze_emotions():
    # Ağır ML kodlarını fonksiyon içinde lazy‐load
    from .emotion_analysis.text import analyze_text_emotion
    from .emotion_analysis.face import analyze_face_emotion
    from .emotion_analysis.fusion import fuse_emotions
    from .music_recommender import recommend_music

    data      = request.json or {}
    text      = data.get("text", "")
    face_data = data.get("face")

    results = {}
    # Metin ve yüz kanalları ayrı ayrı analiz edilir
    if text:
        results["text"] = analyze_text_emotion(text)
    if face_data:
        results["face"] = analyze_face_emotion(face_data)

    if not results:
        return jsonify({"error": "En az bir kanal için veri gönderilmedi."}), 400

    # Füzyon algoritması
    fused      = fuse_emotions(results)
    # Müzik öneri motoru artık id ve title dönecek şekilde düzenlendi
    music_list = recommend_music(fused)  # [{"id": "...", "title": "..."}, ...]

    # Geçici log: Mongo'ya ekle ve hemen sil
    log_doc = {
        "input": data,
        "results": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    }
    inserted = mongo.db.logs.insert_one(log_doc)
    mongo.db.logs.delete_one({"_id": inserted.inserted_id})

    # Sonuçları döndür
    return jsonify({
        "channels": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    })
"""
# app/routes.py

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin     # ← CORS izni için
from .db import mongo

api_bp = Blueprint("api", __name__)

@api_bp.route("/analyze", methods=["POST"])
@cross_origin(origins="*")               # ← Tüm origin’lere izin ver
def analyze_emotions():
    # Ağır ML kodlarını fonksiyon içinde lazy‐load
    from .emotion_analysis.text import analyze_text_emotion
    from .emotion_analysis.face import analyze_face_emotion
    from .emotion_analysis.fusion import fuse_emotions
    from .music_recommender import recommend_music

    data      = request.json or {}
    text      = data.get("text", "")
    face_data = data.get("face")

    results = {}
    # Metin ve yüz kanalları ayrı ayrı analiz edilir
    if text:
        results["text"] = analyze_text_emotion(text)
    if face_data:
        results["face"] = analyze_face_emotion(face_data)

    if not results:
        return jsonify({"error": "En az bir kanal için veri gönderilmedi."}), 400

    # Füzyon algoritması
    fused      = fuse_emotions(results)
    # Müzik öneri motoru her zaman liste döndürsün
    music_list = recommend_music(fused) or []  # Ensure it's always a list

    # Geçici log: Mongo'ya ekle ve hemen sil
    log_doc = {
        "input": data,
        "results": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    }
    inserted = mongo.db.logs.insert_one(log_doc)
    mongo.db.logs.delete_one({"_id": inserted.inserted_id})

    # Sonuçları döndür
    return jsonify({
        "channels": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    })
