# app/music_recommender.py

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import List, Dict, Any

load_dotenv()  # .env içinden YOUTUBE_API_KEY’i alacak

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY environment variable is not set")

# YouTube client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Duygu etiketini arama sorgusuna çevirme
_EMOTION_QUERIES: Dict[str, str] = {
    "mutluluk":  "mutluluk müziği",
    "üzüntü":    "hüzünlü müzik",
    "öfke":      "öfkeli müzik",
    "korku":     "korku atmosfer müziği",
    "şaşkınlık": "şaşkınlık duygusu müziği",
    "tiksinme":  "tiksinme duygusu müziği",
    "nötr":      "dingin müzik"
}

def recommend_music(fused_emotion: Dict[str, Any], max_results: int = 5) -> List[str]:
    """
    fused_emotion: {"label": str, "score": float}
    -> YouTube video ID listesi döner.
    """
    label = fused_emotion.get("label", "nötr")
    query = _EMOTION_QUERIES.get(label, _EMOTION_QUERIES["nötr"])
    
    # YouTube arama
    request = youtube.search().list(
        q=query,
        part="id",
        type="video",
        maxResults=max_results,
        videoCategoryId="10"  # 10 = Music
    )
    response = request.execute()
    
    video_ids = [
        item["id"]["videoId"]
        for item in response.get("items", [])
        if item["id"].get("videoId")
    ]
    return video_ids
