import React, { useState } from 'react';
import EmotionInput from '../EmotionInput';

const HomePage = () => {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Duygu Analizi (Metin + Yüz + Ses)</h1>
      <EmotionInput result={result} setResult={setResult} />

      {/* İsteğe bağlı olarak ayrıntılı metin sonuçlarını da gösterebilirsiniz */}
      {result && (
        <div style={{ marginTop: '1.5rem' }}>
          <h3>🧠 Detaylı Sonuçlar:</h3>
          {result.emotions.text && (
            <p>Metin: {result.emotions.text.label} (%{result.emotions.text.score * 100})</p>
          )}
          {result.emotions.face && (
            <p>Yüz: {result.emotions.face.label} (%{result.emotions.face.score * 100})</p>
          )}
          {result.emotions.audio && (
            <p>Ses: {result.emotions.audio.label} (%{result.emotions.audio.score * 100})</p>
          )}
          {result.fused_emotion && (
            <p>Füzyon: {result.fused_emotion.label} (%{result.fused_emotion.score * 100})</p>
          )}
        </div>
      )}
    </div>
  );
};

export default HomePage;
