# app/music_recommender.py

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from typing import List, Dict

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Her duyguya özel, daha odaklı arama sorguları
_EMOTION_QUERIES: Dict[str, List[str]] = {
    "mutluluk": [
        "upbeat happy pop music",
        "feel good upbeat instrumental",
        "enerjik pozitif şarkılar"
    ],
    "üzüntü": [
        "emotional piano sad music",
        "hüzünlü akustik şarkı",
        "calm sad instrumental"
    ],
    "öfke": [
        "intense rock angry music",
        "öfke dolu heavy metal",
        "enerjik agresif şarkılar"
    ],
    "korku": [
        "scary horror movie soundtrack",
        "gerilim atmosferik müzik",
        "tension build-up music"
    ],
    "şaşkınlık": [
        "surprising reveal epic music",
        "enerjik sürpriz temalı şarkı",
        "unexpected cinematic music"
    ],
    "tiksinme": [
        "dark ambient unsettling music",
        "rahatsız edici tonlar müzik",
        " eerie experimental soundscape"
    ],
    "nötr": [
        "relaxing ambient background music",
        "calm meditation instrumental",
        "dingin rahatlatıcı müzik"
    ]
}

def recommend_music(fused_emotion: dict, max_per_query: int = 2) -> List[str]:
    """
    fused_emotion: {"label": str, "score": float}
    → Duyguya uygun birden fazla sorgudan toplam max_results ID döner.
    """
    label = fused_emotion.get("label", "nötr")
    queries = _EMOTION_QUERIES.get(label, _EMOTION_QUERIES["nötr"])

    video_ids = []
    for query in queries:
        # Her sorgudan max_per_query video çek
        res = youtube.search().list(
            q=query,
            part="id",
            type="video",
            maxResults=max_per_query,
            videoCategoryId="10"
        ).execute()
        for item in res.get("items", []):
            vid = item["id"].get("videoId")
            if vid and vid not in video_ids:
                video_ids.append(vid)

    return video_ids
