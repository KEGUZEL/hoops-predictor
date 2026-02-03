HoopsPredictor: AI-Driven Performance Analyst
============================================

Bu proje, NBA oyuncu ve takımlarının performansını veri odaklı ve yapay zeka destekli şekilde analiz etmek için tasarlanmış tam yığın (full‑stack) bir uygulamadır.

Ana bileşenler:

- Backend: FastAPI (Python) + ML (pandas, scikit-learn / XGBoost)
- Frontend: React tabanlı dashboard (Recharts ile görselleştirme)
- Veri Kaynakları: RapidAPI üzerinden çeşitli NBA istatistik API'leri ve web scraping ile sakatlık/haber verileri
- Veritabanları: PostgreSQL (ilişkisel veriler) + MongoDB veya Redis (anlık sakatlık, yorgunluk vb.)
- DevOps: Docker, Docker Compose, GitHub Actions tabanlı CI/CD, logging & monitoring

Proje yapısı (özet):

- backend/ : FastAPI uygulaması, ingestion job'ları ve ML modeli
- frontend/ : React dashboard arayüzü
- infra/ : Docker Compose, Dockerfile örnekleri ve CI/CD yapılandırmaları

Kurulum ve çalıştırma adımları ileride ayrıntılı olarak eklenecektir.

