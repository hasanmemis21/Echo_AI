import React, { useState } from 'react';
import EmotionInput from '../components/EmotionInput';
import '../styles/HomePage.css';

export default function HomePage() {
  const [result, setResult] = useState(null);

  return (
    <div className="homepage">
      {/* 🎼 Arka planda akan notalar */}
      <div className="notes-container">
        {Array.from({ length: 20 }).map((_, i) => (
          <span key={i} className="note">♪</span>
        ))}
      </div>

      {/* Başlık */}
      <h1>Duygu Analizi + Müzik Öneri</h1>

      {/* 📝 Duygu Giriş Bölümü */}
      <div className="emotion-section">
        <EmotionInput onResults={setResult} />
      </div>

      {/* 📊 Analiz Sonuçları ve Müzik Kartları */}
      {result && (
        <div className="results">
          <div className="details">
            {result.channels?.text && (
              <p>
                📄 Metin: {result.channels.text.label} (
                %{Math.round(result.channels.text.score * 100)})
              </p>
            )}
            {result.channels?.face && (
              <p>
                📷 Yüz: {result.channels.face.label} (
                %{Math.round(result.channels.face.score * 100)})
              </p>
            )}
            {result.fused_emotion && (
              <p>
                🧠 Füzyon: {result.fused_emotion.label} (
                %{Math.round(result.fused_emotion.score * 100)})
              </p>
            )}
          </div>

          <div className="music-list">
            {result.recommended_music.map((uri) => {
              const trackId = uri.split(':').pop();
              return (
                <div key={trackId} className="music-card">
                  <iframe
                    title={trackId}
                    src={`https://open.spotify.com/embed/track/${trackId}`}
                    allow="autoplay; encrypted-media"
                  />
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
