import requests
import json
import os
from dotenv import load_dotenv

# .env dosyasını yükle (API Key'i buradan alacak)
load_dotenv()

# Verilerin kaydedileceği klasör
CACHE_DIR = "cache_data"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def fetch_nba_data(endpoint, params=None):
    """
    Bu fonksiyon API'ye gitmeden önce klasöre bakar.
    Varsa dosyadan okur (KOTA GİTMEZ).
    Yoksa API'den çeker ve kaydeder (1 KOTA GİDER).
    """
    if params is None:
        params = {}

    # 1. Dosya ismi oluştur (örn: games_date-20240212.json)
    # Endpoint'teki eğik çizgileri alt çizgi yapıyoruz ki dosya ismi bozulmasın
    safe_endpoint_name = endpoint.strip("/").replace("/", "_")
    
    # Parametreleri dosya ismine ekliyoruz
    param_str = "_".join([f"{k}-{v}" for k, v in params.items()])
    
    if param_str:
        filename = f"{CACHE_DIR}/{safe_endpoint_name}_{param_str}.json"
    else:
        filename = f"{CACHE_DIR}/{safe_endpoint_name}.json"

    # 2. KONTROL: Bu veri daha önce çekilmiş mi?
    if os.path.exists(filename):
        print(f"📂 [CACHE] Veri yerel dosyadan okunuyor: {filename}")
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    # 3. YOKSA: API'ye İstek At
    print(f"🌐 [API] İnternetten çekiliyor (Kota Harcanıyor)... Endpoint: {endpoint}")
    
    url = f"https://api-nba-v1.p.rapidapi.com/{endpoint.strip('/')}"
    
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        # --- CASUS KOD BAŞLANGICI ---
        if response.status_code == 403:
            print("\n🚨 403 HATASI DETAYI (Bunu bana gönder):")
            print(f"Mesaj: {response.text}") # RapidAPI'nin gönderdiği gizli mesajı yazdır
            print(f"Giden Key (İlk 5 hane): {headers['X-RapidAPI-Key'][:5]}...") 
        # --- CASUS KOD BİTİŞİ ---

        response.raise_for_status() # Hata varsa durdur
        
        data = response.json()

        # 4. KAYDET: Gelecek sefer için sakla
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        return data

    except Exception as e:
        print(f"❌ HATA OLUŞTU: {e}")
        return None