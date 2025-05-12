// src/EmotionInput.js

import React, { useRef, useState, useEffect } from 'react';
import { BACKEND_URL } from './config';
import './styles/EmotionInput.css';

export default function EmotionInput({ result, setResult }) {
  const videoRef = useRef(null);

  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [recording, setRecording] = useState(false);
  const [stream, setStream] = useState(null);
  const [faceImage, setFaceImage] = useState(null);

  // Video <-> stream bağlama
  useEffect(() => {
    if (stream && videoRef.current) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  // Kamerayı kapatma helper
  const stopStream = () => {
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      setStream(null);
    }
  };

  // Bileşen unmount olduğunda kamerayı kapat
  useEffect(() => {
    return () => stopStream();
  }, []);

  // Ses kaydı (yalnızca bir bayrak)
  const startRecording = () => {
    setRecording(true);
    setTimeout(() => setRecording(false), 5000);
  };

  // Kamera aç
  const startCamera = async () => {
    stopStream();
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(s);
      setFaceImage(null);
    } catch (err) {
      console.error('Kamera açma hatası:', err);
      alert('Kameraya erişilemedi: ' + err.message);
    }
  };

  // Anlık kare yakala
  const captureFace = () => {
    if (!stream || !videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    const b64 = canvas.toDataURL('image/jpeg').split(',')[1];
    setFaceImage(b64);
    stopStream();
  };

  // Tüm verileri backend’e gönder ve sonucu al
  const analyzeAll = async () => {
    setLoading(true);
    try {
      const payload = {
        text: text.trim() || null,
        face: faceImage,
        use_audio: recording,
      };
      console.log('🔔 Gönderilen payload:', payload);

      const res = await fetch(`${BACKEND_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      console.log('🔔 Gelen yanıt:', data);
      setResult(data);
    } catch (err) {
      console.error('Analiz hatası:', err);
      alert('Sunucuya bağlanılamadı.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="emotion-input-container">
      {/* Metin Girişi */}
      <textarea
        placeholder="Metni buraya gir..."
        value={text}
        onChange={e => setText(e.target.value)}
        style={{ width: '100%', maxWidth: 400, marginBottom: '1rem' }}
      />

      {/* Yüz: Kamera Kontrolleri */}
      {!stream && (
        <button onClick={startCamera}>Kamerayı Aç</button>
      )}
      {stream && (
        <div style={{ margin: '1rem 0' }}>
          <video ref={videoRef} autoPlay style={{ width: 300 }} />
          <button onClick={captureFace} style={{ marginTop: '0.5rem' }}>
            Kareyi Yakala
          </button>
        </div>
      )}

      {/* Önizleme */}
      {faceImage && (
        <div style={{ margin: '1rem 0' }}>
          <img
            src={`data:image/jpeg;base64,${faceImage}`}
            alt="Yüz önizleme"
            style={{ width: 300, border: '2px solid #444' }}
          />
        </div>
      )}

      {/* Ses Kaydı */}
      <button
        onClick={startRecording}
        disabled={recording}
        style={{ display: 'block', marginBottom: '1rem' }}
      >
        {recording ? 'Ses Kaydediliyor…' : 'Ses Kaydı (5s)'}
      </button>

      {/* Analiz Et */}
      <button
        onClick={analyzeAll}
        disabled={loading}
        style={{ display: 'block', margin: '1rem auto' }}
      >
        {loading ? 'Analiz Ediliyor…' : 'Analiz Et'}
      </button>

      {/* YouTube Önerileri */}
      {result?.recommended_music?.length > 0 && (
        <div className="video-grid" style={{ marginTop: '1.5rem' }}>
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
    </div>
  );
}
