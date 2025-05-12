// src/pages/HomePage.js
import React, { useState } from 'react';
import EmotionInput from '../components/EmotionInput';
import '../styles/HomePage.css';

export default function HomePage() {
  const [result, setResult] = useState(null);
  const [showMusic, setShowMusic] = useState(false);

  return (
    <div className="homepage">
      <h1>Duygu Analizi + Müzik Öneri</h1>
      <EmotionInput onResults={setResult} />

      {result && (
        <div className="results">
          <div className="details">
            {result.channels?.text && (
              <p>📄 Metin: {result.channels.text.label} (%{Math.round(result.channels.text.score*100)})</p>
            )}
            {result.channels?.face && (
              <p>📷 Yüz: {result.channels.face.label} (%{Math.round(result.channels.face.score*100)})</p>
            )}
            {result.fused_emotion && (
              <p>🧠 Füzyon: {result.fused_emotion.label} (%{Math.round(result.fused_emotion.score*100)})</p>
            )}
          </div>

          <button
            className="toggle-music"
            onClick={() => setShowMusic(v => !v)}
          >
            {showMusic ? 'Müzikleri Gizle' : 'Müzikleri Göster'}
          </button>

       {showMusic && result.recommended_music?.length > 0 && (
  <ul className="music-list">
    {(result.recommended_music || []).map((id, idx) => (
      <li key={id || idx}>
        <button
          onClick={() => window.open(`https://youtu.be/${id}`, '_blank')}
        >
          Müzik {idx + 1}
        </button>
      </li>
    ))}
  </ul>
)}
        </div>
      )}
    </div>
  );
}
