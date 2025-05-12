# app/__init__.py

from flask import Flask
from flask_cors import CORS
from .db import mongo

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config["MONGO_URI"] = "mongodb://localhost:27017/duyguai"
    mongo.init_app(app)

    # Burada analiz modüllerini “warm-up” ediyoruz:
    with app.app_context():
        # text
        from .emotion_analysis.text import _get_text_classifier
        _get_text_classifier()
        # face
        from .emotion_analysis.face import _get_face_classifier
        _get_face_classifier()

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return "Flask çalışıyor, analiz modülleri yüklendi."

    return app
