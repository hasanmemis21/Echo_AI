# # app/music_recommender.py

# import os
# from dotenv import load_dotenv
# from googleapiclient.discovery import build
# from typing import List, Dict

# load_dotenv()
# YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
# youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# # Her duyguya özel, daha odaklı arama sorguları
# _EMOTION_QUERIES: Dict[str, List[str]] = {
#     "mutluluk": [
#         "upbeat happy pop music",
#         "feel good upbeat instrumental",
#         "enerjik pozitif şarkılar"
#     ],
#     "üzüntü": [
#         "emotional piano sad music",
#         "hüzünlü akustik şarkı",
#         "calm sad instrumental"
#     ],
#     "öfke": [
#         "intense rock angry music",
#         "öfke dolu heavy metal",
#         "enerjik agresif şarkılar"
#     ],
#     "korku": [
#         "scary horror movie soundtrack",
#         "gerilim atmosferik müzik",
#         "tension build-up music"
#     ],
#     "şaşkınlık": [
#         "surprising reveal epic music",
#         "enerjik sürpriz temalı şarkı",
#         "unexpected cinematic music"
#     ],
#     "tiksinme": [
#         "dark ambient unsettling music",
#         "rahatsız edici tonlar müzik",
#         " eerie experimental soundscape"
#     ],
#     "nötr": [
#         "relaxing ambient background music",
#         "calm meditation instrumental",
#         "dingin rahatlatıcı müzik"
#     ]
# }

# def recommend_music(fused_emotion: dict, max_per_query: int = 2) -> List[str]:
#     """
#     fused_emotion: {"label": str, "score": float}
#     → Duyguya uygun birden fazla sorgudan toplam max_results ID döner.
#     """
#     label = fused_emotion.get("label", "nötr")
#     queries = _EMOTION_QUERIES.get(label, _EMOTION_QUERIES["nötr"])

#     video_ids = []
#     for query in queries:
#         # Her sorgudan max_per_query video çek
#         res = youtube.search().list(
#             q=query,
#             part="id",
#             type="video",
#             maxResults=max_per_query,
#             videoCategoryId="10"
#         ).execute()
#         for item in res.get("items", []):
#             vid = item["id"].get("videoId")
#             if vid and vid not in video_ids:
#                 video_ids.append(vid)

#     return video_ids

# app/music_recommender.py

import os
import logging
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict

# Optional Spotify integration
try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    SPOTIFY_ENABLED = True
except ImportError:
    SPOTIFY_ENABLED = False

load_dotenv()

# YouTube setup
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Spotify setup (Client Credentials Flow)
if SPOTIFY_ENABLED:
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
        spotify = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
        )
    else:
        logging.warning("Spotify credentials not set; falling back to YouTube only.")
        SPOTIFY_ENABLED = False

# Her duyguya özel arama sorguları
_EMOTION_QUERIES: Dict[str, List[str]] = {
    "mutluluk": ["upbeat happy pop music", "feel good upbeat instrumental", "enerjik pozitif şarkılar"],
    "üzüntü": ["emotional piano sad music", "hüzünlü akustik şarkı", "calm sad instrumental"],
    "öfke": ["intense rock angry music", "öfke dolu heavy metal", "enerjik agresif şarkılar"],
    "korku": ["scary horror movie soundtrack", "gerilim atmosferik müzik", "tension build-up music"],
    "şaşkınlık": ["surprising reveal epic music", "enerjik sürpriz temalı şarkı", "unexpected cinematic music"],
    "tiksinme": ["dark ambient unsettling music", "rahatsız edici tonlar müzik", "eerie experimental soundscape"],
    "nötr": ["relaxing ambient background music", "calm meditation instrumental", "dingin rahatlatıcı müzik"]
}


def recommend_music(fused_emotion: dict, max_per_query: int = 2) -> List[str]:
    """
    Duyguya göre önce Spotify'da arama yapar, eğer Spotify kapalıysa YouTube'a döner.
    Returns a list of track URIs (Spotify) or video IDs (YouTube).
    """
    label = fused_emotion.get("label", "nötr")
    queries = _EMOTION_QUERIES.get(label, _EMOTION_QUERIES["nötr"])
    results_list: List[str] = []

    if SPOTIFY_ENABLED:
        # Spotify üzerinden öneri
        try:
            for q in queries:
                resp = spotify.search(q=q, type='track', limit=max_per_query)
                for track in resp.get('tracks', {}).get('items', []):
                    uri = track.get('uri')
                    if uri and uri not in results_list:
                        results_list.append(uri)
            return results_list
        except Exception as e:
            logging.error(f"Spotify API error, falling back to YouTube: {e}")
            # devam et YouTube'a

    # YouTube fallback
    try:
        for query in queries:
            try:
                response = youtube.search().list(
                    q=query,
                    part="id",
                    type="video",
                    maxResults=max_per_query,
                    videoCategoryId="10"
                ).execute()
            except HttpError as e:
                if e.resp.status == 403 and 'quotaExceeded' in str(e):
                    logging.warning("YouTube API quota exceeded, returning empty list.")
                    return []
                logging.error(f"YouTube API error ({e.resp.status}): {e}")
                return []

            items = response.get("items", [])
            for item in items:
                vid = item.get("id", {}).get("videoId")
                if vid and vid not in results_list:
                    results_list.append(vid)
        return results_list

    except Exception as e:
        logging.error(f"Unexpected error in recommend_music: {e}")
        return []
