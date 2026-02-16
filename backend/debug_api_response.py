import requests
import os
from dotenv import load_dotenv

# .env yükle
load_dotenv()

def casus_test():
    print("--- 🕵️ API CASUS TESTİ BAŞLIYOR ---")
    
    # 1. Key Kontrolü
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        print("❌ HATA: .env dosyasında Key BULUNAMADI.")
        return
    
    print(f"🔑 Kullanılan Key: {api_key[:5]}...{api_key[-4:]}")

    # 2. Direkt İstek (Aracı dosya kullanmadan)
    url = "https://api-nba-v1.p.rapidapi.com/games"
    
    # DİKKAT: Tarih formatı YYYY-MM-DD olmalı
    params = {"date": "2024-01-20"}
    
    headers = {
        "X-RapidAPI-Key": api_key.strip(), # Boşlukları temizle
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    print("\n🌐 İstek gönderiliyor...")
    response = requests.get(url, headers=headers, params=params)

    # 3. SONUÇ ANALİZİ
    print(f"📡 Durum Kodu (Status Code): {response.status_code}")

    if response.status_code == 200:
        print("✅ BAŞARILI! Bağlantı sağlandı. Sorun çözülmüş.")
        print(f"Gelen Veri Boyutu: {len(response.text)} karakter")
    elif response.status_code == 403:
        print("⛔ ERİŞİM YASAK (403)!")
        print("👇 İŞTE SEBEBİ (Bunu bana oku):")
        print("------------------------------------------------")
        print(response.text)  # <--- BURASI ÇOK ÖNEMLİ
        print("------------------------------------------------")
    else:
        print("⚠️ Beklenmedik Hata:")
        print(response.text)

if __name__ == "__main__":
    casus_test()