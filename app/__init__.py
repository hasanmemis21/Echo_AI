# app/__init__.py

import os
from dotenv import load_dotenv
import openai
from flask import Flask
from flask_cors import CORS
from .db import mongo

# Ortam değişkenlerini yükle ve OpenAI anahtarını ayarla
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_app():
    app = Flask(__name__)

    # React (://localhost:3000) arayüzünden gelen /api/* çağrılarına izin ver
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # MongoDB bağlantı adresi .env’den okunur; yoksa default localhost
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/duyguai")
    mongo.init_app(app)

    # Blueprint kaydı
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return "Flask çalışıyor, analiz modülleri yüklendi."

    return app
