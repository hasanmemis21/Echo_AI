// src/pages/HomePage.js
import React, { useState } from 'react';
import EmotionInput from '../EmotionInput';

const HomePage = () => {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Duygu Analizi (Metin + Yüz + Ses)</h1>

      <EmotionInput result={result} setResult={setResult} />

      {/* Detaylı kanal sonuçları */}
      {result && (
        <div style={{ marginTop: '1.5rem' }}>
          <h3>🧠 Detaylı Sonuçlar:</h3>

          {/* Metin kanalı */}
          {result.channels?.text && (
            <p>
              <strong>Metin:</strong> {result.channels.text.label}{' '}
              (%{Math.round(result.channels.text.score * 100)})
            </p>
          )}

          {/* Yüz kanalı */}
          {result.channels?.face && (
            <p>
              <strong>Yüz:</strong> {result.channels.face.label}{' '}
              (%{Math.round(result.channels.face.score * 100)})
            </p>
          )}

          {/* Ses kanalı */}
          {result.channels?.audio && (
            <p>
              <strong>Ses:</strong> {result.channels.audio.label}{' '}
              (%{Math.round(result.channels.audio.score * 100)})
            </p>
          )}

          {/* Füzyon sonucu */}
          {result.fused_emotion && (
            <p>
              <strong>Füzyon:</strong> {result.fused_emotion.label}{' '}
              (%{Math.round(result.fused_emotion.score * 100)})
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default HomePage;
