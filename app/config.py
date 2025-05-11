import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki değişkenleri yükle

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/emotionDB")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "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")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

