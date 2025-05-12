// src/pages/HomePage.js
import React, { useState } from 'react';
import EmotionInput from '../components/EmotionInput';
import '../styles/HomePage.css';

export default function HomePage() {
  const [result, setResult] = useState(null);

  return (
    <div className="homepage">
      <h1>Duygu Analizi + Müzik Öneri</h1>
      <EmotionInput onResults={setResult} />

      {result && (
        <div className="results">
          <div className="details">
            {result.channels?.text && (
              <p>📄 Metin: {result.channels.text.label} (%{Math.round(result.channels.text.score * 100)})</p>
            )}
            {result.channels?.face && (
              <p>📷 Yüz: {result.channels.face.label} (%{Math.round(result.channels.face.score * 100)})</p>
            )}
            {result.fused_emotion && (
              <p>🧠 Füzyon: {result.fused_emotion.label} (%{Math.round(result.fused_emotion.score * 100)})</p>
            )}
          </div>

          {/* Müzikler hemen listeleniyor, gömme player ile */}
          {result.recommended_music?.length > 0 && (
            <div className="music-list">
              {result.recommended_music.map((uri) => {
                const trackId = uri.split(':').pop();
                return (
                  <iframe
                    key={trackId}
                    title={trackId}
                    src={`https://open.spotify.com/embed/track/${trackId}`}
                    width="100%"
                    height="80"
                    frameBorder="0"
                    allow="encrypted-media"
                  />
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
