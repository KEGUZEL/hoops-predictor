# Dosya: backend/debug_api_response.py

import json
from app.ingestion.api_clients.api_nba_client import ApiNbaClient

def inspect_raw_response():
    print("--- API TEŞHİS BAŞLIYOR ---")
    client = ApiNbaClient()
    
    # Geçmiş ve oynanmış bir tarih seçelim ki kesin veri olsun (Örn: 20 Ocak 2024)
    test_date = "20240120" 
    
    print(f"Hedef Endpoint: /nba-scoreboard-by-date")
    print(f"Parametre: date={test_date}")
    
    # Client içindeki _get metodunu kullanarak ham veriyi çekiyoruz
    try:
        raw_data = client._get("/nba-scoreboard-by-date", params={"date": test_date})
        
        print("\n--- HAM VERİ TÜRÜ ---")
        print(type(raw_data))
        
        print("\n--- HAM VERİ İÇERİĞİ (İLK 1000 KARAKTER) ---")
        # JSON formatında düzenli görelim
        formatted_json = json.dumps(raw_data, indent=2, ensure_ascii=False)
        print(formatted_json[:2000]) # Çok uzunsa terminali kilitlemesin diye kesiyoruz
        
        print("\n--- ANAHTARLAR (KEYS) ---")
        if isinstance(raw_data, dict):
            print(raw_data.keys())
        elif isinstance(raw_data, list) and len(raw_data) > 0:
            print(f"Liste uzunluğu: {len(raw_data)}")
            if isinstance(raw_data[0], dict):
                print(f"Listedeki ilk öğenin keyleri: {raw_data[0].keys()}")
                
    except Exception as e:
        print(f"\n!!! HATA OLUŞTU !!!: {e}")

if __name__ == "__main__":
    inspect_raw_response()