Çok Modlu Duygu Analizi ile Müzik Öneri Sistemi

Bu proje, kullanıcının ses, yüz ifadesi ve metin girdilerinden gerçek zamanlı duygu analizi yaparak, elde edilen içgörüye göre müzik önerileri sunan bir web uygulamasıdır.

📚 Özellikler

Ses Analizi: Audio dosyalarından ses tonu, enerji, tempo ve pitch özelliklerini çıkarır.

Yüz İfadesi Tanıma: Webcam görüntüsünden mutlu, üzgün, öfkeli, korkmuş, şaşkın, tiksinmiş ve nötr duyguları tespit eder.

Metin Analizi: Kullanıcı tarafından girilen metinlerin duygu durumunu sınıflandırır.

Füzyon Algoritması: Üç veri kaynağı skorlarını ağırlıklı olarak birleştirerek tek bir duygu çıktısı üretir.

Müzik Öneri Motoru: Duygulara uygun müzik parçalarını Spotify üzerinden embed oynatıcı ile sunar.

Geri Bildirim Mekanizması: Beğeni/Beğenmeme butonlarıyla kullanıcı geri bildirimleri toplanır.

Performans İzleme: API yanıt süreleri X-Response-Time header’ında ve loglarda takip edilir.

Responsive UI: Mobil ve tablet uyumluluğu için media query tabanlı tek sütun düzeni.

🚀 Kurulum

Depoyu klonlayın:

git clone https://github.com/kullanici/duygu-muzik-onerisi.git
cd duygu-muzik-onerisi

Sanal ortam oluşturun ve aktive edin:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

Gereksinimleri yükleyin:

pip install -r requirements.txt

Ortam değişkenlerini .env dosyasına ekleyin:
MONGO_URI=mongodb://localhost:27017/emotionDB
HUGGINGFACE_API_KEY=your_hf_key
YOUTUBE_API_KEY=your_youtube_key

📁 Proje Yapısı
├── app/                  # Backend kaynak kodu
│   ├── emotion_analysis/ # Duygu analizi modülleri (audio, face, text, fusion)
│   ├── routes.py         # Flask API uç noktaları
│   ├── db.py             # MongoDB bağlantı ayarları
│   ├── config.py         # Ortam konfigürasyonları
│   └── music_recommender.py
├── frontend/             # React uygulaması
│   ├── src/
│   └── package.json
├── tests/                # Pytest birim ve entegrasyon testleri
├── run.py                # Flask uygulama oluşturucu
├── requirements.txt      # Python paket gereksinimleri
└── README.md 

🔧 Usage
Backend’i başlat:

python run.py

Frontend’i başlat:

cd frontend
npm install
npm start

Tarayıcıda http://localhost:3000 adresine gidin.

🧪 Testler
Tüm testleri çalıştırmak için:
python -m pytest

Performans testi:
python -m pytest tests/test_api.py::test_analyze_performance -s

📜 API Endpoints

Yol

Yöntem

Açıklama

/api/analyze

POST

Text/face/audio veri alır, duygu analizi ve öneri döner.

/api/feedback

POST

track_id ve liked alanlarıyla kullanıcı geri bildirimi alır.

Örnek /api/analyze isteği (JSON):
{
  "text": "Mutluyum",
  "audio": "<base64 ses>"
}
