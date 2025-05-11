from flask import Flask
from .db import mongo  # app/db.py dosyasındaki mongo nesnesi

def create_app():
    app = Flask(__name__)

    # MongoDB bağlantı adresi (gerekirse 'duyguai' yerine kendi db adını kullan)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/duyguai"

    # Mongo eklentisini Flask'e bağla
    mongo.init_app(app)

    # Routes (API) blueprint'ini dahil et
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return "Flask çalışıyor, analiz modülleri yüklendi."

    return app
