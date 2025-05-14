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
# # app/routes.py

# from flask import Blueprint, request, jsonify
# from flask_cors import cross_origin     # ← CORS izni için
# from .db import mongo

# api_bp = Blueprint("api", __name__)

# @api_bp.route("/analyze", methods=["POST"])
# @cross_origin(origins="*")
# def analyze_emotions():
#     # Lazy‐load ML code
#     from .emotion_analysis.text import analyze_text_emotion
#     from .emotion_analysis.face import analyze_face_emotion
#     from .emotion_analysis.audio import (
#         analyze_audio_emotion_from_base64
#     )
#     from .emotion_analysis.fusion import fuse_emotions
#     from .music_recommender import recommend_music
#     import base64

#     data      = request.json or {}
#     text      = data.get("text", "")    # Text channel
#     face_data = data.get("face")        # Face channel (Base64)
#     audio_b64 = data.get("audio")       # Audio channel (Base64)

#     results = {}
#     if text:
#         results["text"] = analyze_text_emotion(text)
#     if face_data:
#         results["face"] = analyze_face_emotion(face_data)
#     if audio_b64:
#         results["audio"] = analyze_audio_emotion_from_base64(audio_b64)

#     if not results:
#         return jsonify({"error": "En az bir kanal için veri gönderilmedi."}), 400

#     fused      = fuse_emotions(results)
#     music_list = recommend_music(fused) or []

#     # Log-and-forget
#     log_doc = {
#         "input": data,
#         "results": results,
#         "fused_emotion": fused,
#         "recommended_music": music_list
#     }
#     inserted = mongo.db.logs.insert_one(log_doc)
#     mongo.db.logs.delete_one({"_id": inserted.inserted_id})

#     return jsonify({
#         "channels": results,
#         "fused_emotion": fused,
#         "recommended_music": music_list
#     })

import io
import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from .db import mongo
import time
from .emotion_analysis.audio import (
    analyze_audio_emotion_from_base64,
    analyze_audio_emotion_from_bytes
)
from .emotion_analysis.text import analyze_text_emotion
from .emotion_analysis.face import analyze_face_emotion
from .emotion_analysis.fusion import fuse_emotions
from .music_recommender import recommend_music
from pydub.utils import which

api_bp = Blueprint("api", __name__)
logging.basicConfig(level=logging.DEBUG)

@api_bp.route("/analyze", methods=["POST"])
@cross_origin(origins="*")
def analyze_emotions():
    # Zaman ölçümüne başla
    start = time.monotonic()
    # ffmpeg’in Python’dan erişilebilir olduğunu kontrol et
    logging.debug("FFmpeg yolu (routes): %s", which("ffmpeg"))

    data = {}
    if request.is_json:
        data = request.get_json()

    results = {}

    # 1) Text
    text = data.get("text", "")
    if text:
        results["text"] = analyze_text_emotion(text)

    # 2) Face
    face_data = data.get("face")
    if face_data:
        results["face"] = analyze_face_emotion(face_data)

    # 3) Audio: öncelik form‐data dosyası, sonra JSON b64
    audio_file = request.files.get("audio_file")
    if audio_file:
        raw = audio_file.read()
        results["audio"] = analyze_audio_emotion_from_bytes(raw)
    else:
        audio_b64 = data.get("audio")
        if audio_b64:
            results["audio"] = analyze_audio_emotion_from_base64(audio_b64)

    if not results:
        return jsonify({"error": "En az bir kanal için veri gönderilmedi."}), 400

    # 4) Fusion & müzik önerisi
    fused      = fuse_emotions(results)
    music_list = recommend_music(fused) or []
    # Süreyi hesapla ve logla
    elapsed = time.monotonic() - start
    logging.info(f"/analyze tamamlandı in {elapsed:.3f}s")

    # Loglama (geçici)
    log_doc = {
        "input": data,
        "results": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    }
    inserted = mongo.db.logs.insert_one(log_doc)
    mongo.db.logs.delete_one({"_id": inserted.inserted_id})

    return jsonify({
        "channels": results,
        "fused_emotion": fused,
        "recommended_music": music_list
    }), 200, {'X-Response-Time': f'{elapsed:.3f}'}

# Yeni: Feedback endpoint
@api_bp.route("/feedback", methods=["POST"])
@cross_origin(origins="*")
def feedback():
    data = request.get_json() or {}
    track_id = data.get("track_id")
    liked    = bool(data.get("liked"))

    if not track_id:
        return jsonify({"error":"track_id eksik"}), 400

    mongo.db.feedback.insert_one({
        "track_id": track_id,
        "liked": liked
    })
    return jsonify({"status":"ok"})