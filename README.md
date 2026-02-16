# 🏀 Hoops Predictor - AI Destekli NBA Analiz Sistemi

Hoops Predictor, NBA oyuncularının performanslarını analiz eden, sakatlık risklerini değerlendiren ve yapay zeka destekli maç tahminleri sunan kapsamlı bir analiz platformudur.

Backend tarafında **FastAPI** ve Python, Frontend tarafında **React** ve Vite, altyapı olarak **Docker** kullanılmaktadır.

---

## 🚀 Özellikler

* **📊 Oyuncu Analizi:** Geçmiş maç verilerine dayalı detaylı istatistikler.
* **🤖 AI Tahminleri:** Makine öğrenmesi ile oyuncu performans tahminleri.
* **🏥 Sakatlık Takibi:** Güncel sakatlık raporları ve risk analizleri (ESPN & Rotowire entegrasyonu).
* **🛡️ Takım Risk Paneli:** Takımların genel sağlık ve performans risk durumu.
* **⚡ Hızlı ve Modern:** FastAPI ve React ile geliştirilmiş yüksek performanslı mimari.

---

## 🛠 Gereksinimler

Projeyi çalıştırmadan önce bilgisayarınızda şunların kurulu olması gerekir:

* [Docker Desktop](https://www.docker.com/products/docker-desktop) (Önerilen)
* [Python 3.10+](https://www.python.org/)
* [Node.js 18+](https://nodejs.org/)
* **RapidAPI Hesabı** (Verileri çekmek için)

---

## 🔑 Kurulum Öncesi: API Anahtarı (ÇOK ÖNEMLİ!) ⚠️

Bu proje **API-NBA** servisini kullanır. API'nin çalışması için sadece key almak yetmez, **abone olmanız şarttır**.

1.  [RapidAPI - API-NBA Pricing](https://rapidapi.com/api-sports/api/api-nba/pricing) sayfasına gidin.
2.  **Basic (Free)** paketi altındaki **"Subscribe"** butonuna tıklayın. (Bunu yapmazsanız `403 Forbidden` hatası alırsınız).
3.  Abonelik tamamlandıktan sonra **Endpoints** sekmesinden `X-RapidAPI-Key` değerinizi kopyalayın.

---

## ⚙️ Kurulum ve Çalıştırma

### 1. Projeyi Klonlayın

```bash
git clone [https://github.com/kullaniciadi/hoops-predictor.git](https://github.com/kullaniciadi/hoops-predictor.git)
cd hoops-predictor

backend klasörünün içine .env adında bir dosya oluşturun ve aşağıdaki bilgileri yapıştırın:

Dosya: backend/.env

# RapidAPI Ayarları
RAPIDAPI_KEY=BURAYA_RAPIDAPI_KEYINIZI_YAPISTIRIN
RAPIDAPI_HOST=api-nba-v1.p.rapidapi.com

# Veritabanı Ayarları (Docker kullanacaksanız değiştirmeyin)
MONGODB_URL=mongodb://mongo:27017/hoops_db
SECRET_KEY=supersecretkey
PROJECT_NAME=HoopsPredictor

3. Docker ile Çalıştırma (Önerilen)
Tüm sistemi (Backend, Frontend ve Veritabanı) tek komutla ayağa kaldırmak için ana dizinde şu komutu çalıştırın:

Bash

docker-compose -f infra/docker-compose.yml up --build

Kurulum bittiğinde şu adreslerden erişebilirsiniz:

Frontend (Uygulama): http://localhost:5173

Backend (API Docs): http://localhost:8000/docs


cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

cd frontend
npm install
npm run dev