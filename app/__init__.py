# app/__init__.py (başlangıç için sade sürüm)
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "✅ Flask çalışıyor!"

    return app
