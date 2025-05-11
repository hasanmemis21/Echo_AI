import React, { useState } from 'react';
import EmotionInput from '../EmotionInput';

const HomePage = () => {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Duygu Analizi (Metin + Yüz)</h1>

      <textarea
        rows={4}
        cols={50}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Metni buraya giriniz..."
        style={{ display: "block", marginBottom: "1rem" }}
      />

      <EmotionInput text={text} setResult={setResult} />

      {result && (
        <div style={{ marginTop: '2rem' }}>
          <h3>🧠 Tahmin Edilen Duygular:</h3>

          {result.emotions?.text && (
            <p><strong>Metin:</strong> {result.emotions.text.label} (%{Math.round(result.emotions.text.score * 100)})</p>
          )}

          {result.emotions?.face && (
            <p><strong>Yüz:</strong> {result.emotions.face.label} (%{Math.round(result.emotions.face.score * 100)})</p>
          )}

          {result.fused_emotion && (
            <p><strong>Birleşik Duygu (Fused):</strong> {result.fused_emotion.label} (%{Math.round(result.fused_emotion.score * 100)})</p>
          )}

          {result.recommended_music && result.recommended_music.length > 0 && (
            <>
              <h4>🎵 Önerilen Müzikler:</h4>
              <ul>
                {result.recommended_music.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default HomePage;
