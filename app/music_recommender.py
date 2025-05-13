# app/music_recommender.py

import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List, Dict

# Load Spotify credentials from environment
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise RuntimeError("Missing Spotify credentials: set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your .env file")

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Predefined mood-to-query mappings
_EMOTION_QUERIES: Dict[str, List[str]] = {
    "mutluluk": [
        "happy upbeat pop",
        "feel good instrumental",
        "sunny day music"
    ],
    "üzüntü": [
        "sad piano instrumental",
        "melancholic acoustic",
        "emotional ballad"
    ],
    "öfke": [
        "angry rock music",
        "intense heavy metal",
        "aggressive guitar"
    ],
    "korku": [
        "horror ambient soundscape",
        "dark cinematic tension",
        "eerie suspense music"
    ],
    "şaşkınlık": [
        "epic surprise soundtrack",
        "bright orchestral reveal",
        "unexpected cinematic"
    ],
    "tiksinme": [
        "dark ambient unsettling",
        "experimental dissonant",
        "haunting soundscape"
    ],
    "nötr": [
        "relaxing ambient music",
        "calm meditation track",
        "chill lo-fi beats"
    ]
}


def recommend_music(
    fused_emotion: dict,
    num_tracks: int = 6
) -> List[str]:
    """
    Fetches a randomized set of Spotify track URIs matching the detected emotion.

    :param fused_emotion: {'label': str, 'score': float}
    :param num_tracks: number of tracks to return
    :return: List of Spotify track URIs
    """
    label = fused_emotion.get("label", "nötr")
    # Pick one of the related queries at random
    queries = _EMOTION_QUERIES.get(label, _EMOTION_QUERIES["nötr"])
    query = random.choice(queries)

    # Search Spotify for tracks matching the query
    try:
        response = sp.search(q=query, type="track", limit=50)
        items = response.get("tracks", {}).get("items", [])
    except Exception as e:
        # On API error, return empty list
        print(f"Spotify search error: {e}")
        return []

    if not items:
        return []

    # Shuffle and take top N
    random.shuffle(items)
    selected = items[:num_tracks]
    # Return Spotify URIs (e.g. spotify:track:...) for embedding
    return [track.get("uri") for track in selected if track.get("uri")]
