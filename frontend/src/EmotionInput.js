import React, { useRef, useState } from 'react';
import { BACKEND_URL } from './config';

const EmotionInput = ({ text, setResult }) => {
  const videoRef = useRef(null);
  const [loading, setLoading] = useState(false);

  const captureAndAnalyze = async (withAudio = false) => {
    setLoading(true);
    try {
      let base64Image = null;

      if (videoRef.current && videoRef.current.srcObject) {
        const video = videoRef.current;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/jpeg');
        base64Image = imageData.split(',')[1];
      }

      const response = await fetch(`${BACKEND_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text || null,
          face: base64Image,
          use_audio: withAudio
        })
      });

      const data = await response.json();
      console.log("Gelen veri:", data);
      setResult(data);
    } catch (error) {
      console.error("Analiz hatası:", error);
      alert("Sunucuya bağlanılamadı.");
    }
    setLoading(false);
  };

  const startCamera = () => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch((err) => {
        console.error("Kamera açılamadı:", err);
        alert("Kameraya erişilemedi.");
      });
  };

  return (
    <div style={{ marginTop: "1rem" }}>
      <button onClick={startCamera}>Kamerayı Aç</button>
      <video ref={videoRef} autoPlay style={{ width: "300px", marginTop: "1rem" }}></video>
      <div>
        <button onClick={() => captureAndAnalyze(false)} disabled={loading} style={{ marginTop: "1rem", marginRight: "0.5rem" }}>
          {loading ? "Analiz Ediliyor..." : "Kareyi Yakala ve Analiz Et"}
        </button>
        <button onClick={() => captureAndAnalyze(true)} disabled={loading} style={{ marginTop: "1rem" }}>
          {loading ? "Ses Analizi Yapılıyor..." : "Mikrofonla Ses Analizi Yap"}
        </button>
      </div>
    </div>
  );
};

export default EmotionInput;
