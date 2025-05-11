import React, { useRef, useState } from 'react';
import { BACKEND_URL } from './config';
import './styles/EmotionInput.css';

export default function EmotionInput({ result, setResult }) {
  const videoRef = useRef(null);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);

  // Client-side ses kaydı (5s)
  const startRecording = () => {
    setRecording(true);
    setTimeout(() => setRecording(false), 5000);
  };

  const captureAndAnalyze = async () => {
    setLoading(true);
    let base64Image = null;

    // Yüz modu için
    if (videoRef.current && videoRef.current.srcObject) {
      const video = videoRef.current;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
      base64Image = canvas.toDataURL('image/jpeg').split(',')[1];
    }

    try {
      const payload = {
        text: text || null,
        face: base64Image,
        use_audio: recording
      };

      const res = await fetch(`${BACKEND_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert('Sunucuya bağlanılamadı.');
    }

    setLoading(false);
  };

  const startCamera = () => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => { videoRef.current.srcObject = stream; })
      .catch(() => alert('Kameraya erişilemedi.'));
  };

  return (
    <>
      <div className="input-modes">
        {/* Metin */}
        <div className="mode">
          <h4>Metin</h4>
          <textarea
            placeholder="Metni buraya girin..."
            value={text}
            onChange={e => setText(e.target.value)}
          />
        </div>

        {/* Yüz */}
        <div className="mode">
          <h4>Yüz</h4>
          <button onClick={startCamera}>Kamerayı Aç</button>
          <video ref={videoRef} autoPlay />
        </div>

        {/* Ses */}
        <div className="mode">
          <h4>Ses</h4>
          <button
            className="record"
            onClick={startRecording}
            disabled={recording}
          >
            {recording ? 'Kaydediliyor…' : 'Ses Kaydı (5s)'}
          </button>
        </div>
      </div>

      <button
        className="analyze-button"
        onClick={captureAndAnalyze}
        disabled={loading}
      >
        {loading ? 'Analiz Ediliyor…' : 'Analiz Et'}
      </button>

      {/* YouTube önerileri */}
      {result?.recommended_music?.length > 0 && (
        <div className="video-grid">
          {result.recommended_music.map(id => (
            <iframe
              key={id}
              src={`https://www.youtube.com/embed/${id}?autoplay=1`}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              title={id}
            />
          ))}
        </div>
      )}
    </>
  );
}
