import React, { useState, useRef, useEffect } from 'react';
import { BACKEND_URL } from '../config';
import '../styles/EmotionInput.css';

export default function EmotionInput({ onResults }) {
  const [text, setText] = useState('');
  const [stream, setStream] = useState(null);
  const [imageData, setImageData] = useState(null);
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const [audioUrl, setAudioUrl] = useState('');
  const [audioBase64, setAudioBase64] = useState('');
  const [loading, setLoading] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Kamera aç
  const openCamera = async () => {
    const s = await navigator.mediaDevices.getUserMedia({ video: true });
    setStream(s);
    videoRef.current.srcObject = s;
    await videoRef.current.play();
    setImageData(null);
  };

  // Fotoğrafı yakala
  const capturePhoto = () => {
    if (!stream) return;
    const video = videoRef.current;
    canvasRef.current.width = video.videoWidth;
    canvasRef.current.height = video.videoHeight;
    const ctx = canvasRef.current.getContext('2d');
    ctx.drawImage(video, 0, 0);
    const b64 = canvasRef.current.toDataURL('image/png').split(',')[1];
    setImageData(b64);
    // istersen kamerayı kapat:
    stream.getTracks().forEach(t => t.stop());
    setStream(null);
  };

  // Ses kaydı başlat
  const startRecording = async () => {
    const s = await navigator.mediaDevices.getUserMedia({ audio: true });
    chunksRef.current = [];
    const recorder = new MediaRecorder(s);
    recorder.ondataavailable = e => e.data.size && chunksRef.current.push(e.data);
    recorder.onstop = () => {
      s.getTracks().forEach(t => t.stop());
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
      const r = new FileReader();
      r.onloadend = () => setAudioBase64(r.result.split(',')[1]);
      r.readAsDataURL(blob);
      setRecording(false);
    };
    recorder.start();
    mediaRecorderRef.current = recorder;
    setRecording(true);
    setAudioUrl('');
    setAudioBase64('');
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current = null;
    }
  };

  // Analiz isteği
  const analyze = async () => {
    if (recording) {
      alert('Ses kaydını önce durdurun.');
      return;
    }
    if (!text && !imageData && !audioBase64) {
      alert('En az birini girin: metin, fotoğraf veya ses.');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text || null,
          face: imageData || null,
          audio: audioBase64 || null,
          use_audio: Boolean(audioBase64)
        })
      });
      const json = await res.json();
      onResults(json);
      // Temizle
      setText('');
      setImageData(null);
      setAudioUrl('');
      setAudioBase64('');
    } catch (e) {
      console.error(e);
      alert('Analiz sırasında hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="emotion-input">
      <textarea
        className="emotion-input__text"
        placeholder="Metni buraya girin"
        value={text}
        onChange={e => setText(e.target.value)}
      />

      <div className="emotion-input__controls">
        <div className="control-block">
          <button onClick={openCamera} disabled={loading}>
            Kamera Aç
          </button>
          <button onClick={capturePhoto} disabled={!stream || loading}>
            Fotoğraf Çek
          </button>
          <video ref={videoRef} style={{ width: 160, marginTop: 8 }} />
          <canvas ref={canvasRef} style={{ display: 'none' }} />
        </div>

        <div className="control-block">
          <button onClick={startRecording} disabled={recording || loading}>
            {recording ? 'Kaydediliyor…' : 'Ses Kaydı Başlat'}
          </button>
          <button onClick={stopRecording} disabled={!recording || loading}>
            Durdur
          </button>
          {audioUrl && <audio controls src={audioUrl} style={{ marginTop: 8 }} />}
        </div>
      </div>

      <button
        className="emotion-input__analyze"
        onClick={analyze}
        disabled={loading}
      >
        {loading ? 'Analiz Ediliyor…' : 'Analiz Et'}
      </button>
    </div>
  );
}
