

// import React, { useState } from 'react';
// import EmotionInput from '../components/EmotionInput';
// import '../styles/HomePage.css';

// export default function HomePage() {
//   const [result, setResult] = useState(null);

//   // 🎼 20 nota için rastgele parametreler oluştur
//   const notes = Array.from({ length: 20 }).map((_, i) => ({
//     id: i,
//     left: Math.random() * 100,              // yatay yüzde konum
//     fallDur: 8 + Math.random() * 6,         // 8–14 saniye arası düşme süresi
//     swayDur: 3 + Math.random() * 3,         // 3–6 saniye arası yalpalanma süresi
//     size: 16 + Math.random() * 24,          // 16–40px arası ikon boyutu
//     color: `hsl(${Math.random() * 360}, 80%, 75%)` // rastgele pastel renk
//   }));

//   return (
//     <div className="homepage">
//       {/* 🎼 Arka planda akan notalar */}
//       <div className="notes-container">
//         {notes.map(n => (
//           <span
//             key={n.id}
//             className="note"
//             style={{
//               left: `${n.left}%`,           // CSS değişkenlerini inline set ediyoruz
//               '--fall-dur': `${n.fallDur}s`,
//               '--sway-dur': `${n.swayDur}s`,
//               '--note-size': `${n.size}px`,
//               '--note-color': n.color
//             }}
//           >
//             ♪
//           </span>
//         ))}
//       </div>

//       {/* Başlık */}
//       <h1>Duygu Analizi + Müzik Öneri</h1>

//       {/* 📝 Duygu Giriş Bölümü */}
//       <div className="emotion-section">
//         <EmotionInput onResults={setResult} />
//       </div>

//       {/* 📊 Analiz Sonuçları ve Müzik Kartları */}
//       {result && (
//         <div className="results">
//           <div className="details">
//             {result.channels?.text && (
//               <p>
//                 📄 Metin: {result.channels.text.label} (
//                 %{Math.round(result.channels.text.score * 100)})
//               </p>
//             )}
//             {result.channels?.face && (
//               <p>
//                 📷 Yüz: {result.channels.face.label} (
//                 %{Math.round(result.channels.face.score * 100)})
//               </p>
//             )}
//             {result.fused_emotion && (
//               <p>
//                 🧠 Füzyon: {result.fused_emotion.label} (
//                 %{Math.round(result.fused_emotion.score * 100)})
//               </p>
//             )}
//           </div>

//           <div className="music-list">
//             {result.recommended_music.map((uri) => {
//               const trackId = uri.split(':').pop();
//               return (
//                 <div key={trackId} className="music-card">
//                   <iframe
//                     title={trackId}
//                     src={`https://open.spotify.com/embed/track/${trackId}`}
//                     allow="autoplay; encrypted-media"
//                   />
//                 </div>
//               );
//             })}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

import React, { useState } from 'react';
import EmotionInput from '../components/EmotionInput';
import '../styles/HomePage.css';
// Recharts imports
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function HomePage() {
  const [result, setResult] = useState(null);

  // 🎼 20 nota için rastgele parametreler oluştur
  const notes = Array.from({ length: 20 }).map((_, i) => ({
    id: i,
    left: Math.random() * 100,              // yatay yüzde konum
    fallDur: 8 + Math.random() * 6,         // 8–14 saniye arası düşme süresi
    swayDur: 3 + Math.random() * 3,         // 3–6 saniye arası yalpalanma süresi
    size: 16 + Math.random() * 24,          // 16–40px arası ikon boyutu
    color: `hsl(${Math.random() * 360}, 80%, 75%)` // rastgele pastel renk
  }));

  // Grafiğe veri
  const chartData = result
    ? [
        result.channels.text && { name: 'Metin', value: Math.round(result.channels.text.score * 100) },
        result.channels.audio && { name: 'Ses', value: Math.round(result.channels.audio.score * 100) },
        result.channels.face && { name: 'Yüz', value: Math.round(result.channels.face.score * 100) }
      ].filter(Boolean)
    : [];

  return (
    <div className="homepage">
      {/* 🎼 Arka planda akan notalar */}
      <div className="notes-container">
        {notes.map(n => (
          <span
            key={n.id}
            className="note"
            style={{
              left: `${n.left}%`,
              '--fall-dur': `${n.fallDur}s`,
              '--sway-dur': `${n.swayDur}s`,
              '--note-size': `${n.size}px`,
              '--note-color': n.color
            }}
          >
            ♪
          </span>
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
              <p>📄 Metin: {result.channels.text.label} (%{Math.round(result.channels.text.score * 100)})</p>
            )}
            {result.channels?.face && (
              <p>📷 Yüz: {result.channels.face.label} (%{Math.round(result.channels.face.score * 100)})</p>
            )}
            {result.fused_emotion && (
              <p>🧠 Füzyon: {result.fused_emotion.label} (%{Math.round(result.fused_emotion.score * 100)})</p>
            )}
          </div>

          {/* Yatay yerleşim: müzik ve grafik */}
          <div className="results-content">
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

            <div className="chart-container">
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 100]} tickFormatter={v => `${v}%`} />
                  <Tooltip formatter={value => `${value}%`} />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
