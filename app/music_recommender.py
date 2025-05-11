import requests
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # .env dosyasından alınır

def search_youtube_video(query):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 1
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        video_id = data["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/embed/{video_id}"
    else:
        return None


def recommend_music(emotion_label):
    emotion_music_keywords = {
        "mutluluk": "happy upbeat song",
        "üzüntü": "sad emotional song",
        "öfke": "angry rock song",
        "korku": "scary suspense music",
        "şaşkınlık": "surprise theme music",
        "tiksinme": "dark experimental music",
        "nötr": "chill background music",
        "sevgi": "romantic love song"
    }

    keyword = emotion_music_keywords.get(emotion_label.lower(), "calm instrumental music")
    video_url = search_youtube_video(keyword)

    return [video_url] if video_url else ["Müzik bulunamadı."]
