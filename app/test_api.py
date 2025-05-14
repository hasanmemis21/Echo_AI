import io
import json
import pytest
from run import create_app
from app.db import mongo

@pytest.fixture
def client(monkeypatch):
    app = create_app()
    app.config['TESTING'] = True
    # Initialize PyMongo with app context for tests
    mongo.init_app(app)
    client = app.test_client()
    return client

def test_analyze_no_data(client):
    resp = client.post('/api/analyze', json={})
    assert resp.status_code == 400
    body = resp.get_json()
    assert "error" in body

def test_analyze_text_only(client):
    resp = client.post('/api/analyze', json={"text":"Mutluyum"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert "channels" in body
    assert "text" in body["channels"]
    assert "fused_emotion" in body
    assert isinstance(body["recommended_music"], list)

def test_feedback_endpoint(client):
    resp = client.post('/api/feedback', json={})
    assert resp.status_code == 400

    resp = client.post('/api/feedback',
                       json={"track_id":"abcd1234","liked":True})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body == {"status":"ok"}

    # Cleanup inserted feedback
    entry = mongo.db.feedback.find_one({"track_id":"abcd1234"})
    assert entry["liked"] is True
    mongo.db.feedback.delete_one({"_id": entry["_id"]})
