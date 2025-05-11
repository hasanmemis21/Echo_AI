# app/__init__.py
from flask import Flask
from flask_cors import CORS
from .db import mongo

def create_app():
    app = Flask(__name__)

    # React (3000) arayüzünden gelen API çağrılarına izin ver
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # MongoDB bağlantı adresi
    app.config["MONGO_URI"] = "mongodb://localhost:27017/duyguai"
    mongo.init_app(app)

    # Routes blueprint’ini kaydet
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return "Flask çalışıyor, analiz modülleri yüklendi."

    return app
