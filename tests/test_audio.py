# app/emotion_analysis/test_audio.py

import os
import io
import pytest
import base64
from audio import extract_audio_features, analyze_audio_emotion_from_bytes

@pytest.fixture
def sample_wav_bytes():
    path = os.path.join(os.path.dirname(__file__), "data", "audio", "sample.wav")
    with open(path, "rb") as f:
        return f.read()

@pytest.fixture
def sample_m4a_bytes():
    path = os.path.join(os.path.dirname(__file__), "data", "audio", "sample.m4a")
    with open(path, "rb") as f:
        return f.read()

def test_extract_audio_features_wav(sample_wav_bytes):
    features = extract_audio_features(sample_wav_bytes)
    assert isinstance(features, dict)
    assert set(features.keys()) == {"energy", "tempo_bpm", "pitch_hz"}

def test_extract_audio_features_m4a(sample_m4a_bytes):
    features = extract_audio_features(sample_m4a_bytes)
    assert isinstance(features, dict)
    assert set(features.keys()) == {"energy", "tempo_bpm", "pitch_hz"}

def test_analyze_audio_emotion_from_bytes_wav(sample_wav_bytes):
    result = analyze_audio_emotion_from_bytes(sample_wav_bytes)
    # Hem duygu hem de özellikler dönüyor mu?
    assert "emotion" in result and "features" in result
    assert isinstance(result["emotion"], dict)
    assert isinstance(result["features"], dict)

def test_analyze_audio_emotion_from_bytes_m4a(sample_m4a_bytes):
    result = analyze_audio_emotion_from_bytes(sample_m4a_bytes)
    assert "emotion" in result and "features" in result
    assert isinstance(result["emotion"], dict)
    assert isinstance(result["features"], dict)
