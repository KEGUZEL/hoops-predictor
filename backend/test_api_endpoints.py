from app.ingestion.api_clients.api_nba_client import ApiNbaClient

def test_endpoints():
    client = ApiNbaClient()
    
    # Test için geçerli bir tarih (Geçmiş bir tarih seçelim ki maç olsun)
    test_params = {"date": "2024-01-20"} 
    
    candidates = [
        # --- Olasılık 1: Tireli İsimler ---
        "/nba-fixtures",
        "/nba-schedule",
        "/nba-games",
        "/nba-scoreboard",
        "/nba-livescore",
        "/nba-results",
        
        # --- Olasılık 2: Tiresiz İsimler ---
        "/nbafixtures",
        "/nbaschedule",
        "/nbagames",
        "/nbascoreboard",
        "/nbalivescore",
        
        # --- Olasılık 3: Sade İsimler ---
        "/fixtures",
        "/schedule",
        "/games",
        "/matches",
        "/scores",
        
        # --- Olasılık 4: 'List' eki ---
        "/nba-list-games",
        "/nba-game-list"
    ]
    
    print(f"Testing endpoints with params: {test_params}...")
    print("=" * 60)
    
    for endpoint in candidates:
        try:
            # Parametre ile istek atıyoruz
            data = client._get(endpoint, params=test_params)
            
            # Eğer buraya gelirse hata almamış demektir
            print(f"🌟 {endpoint} -> ÇALIŞTI! (Data tipi: {type(data)})")
            
            # İçinde veri var mı diye kısaca bakalım
            if isinstance(data, dict):
                print(f"   Keys: {list(data.keys())[:3]}")
            elif isinstance(data, list) and len(data) > 0:
                print(f"   İlk eleman: {data[0]}")
                
        except Exception as e:
            # Sadece 404 olmayan hataları veya başarılı sonuçları önemsiyoruz
            error_msg = str(e)
            if "404" in error_msg:
                pass # 404'leri ekrana basıp kalabalık yapmayalım
            else:
                print(f"❓ {endpoint} -> Farklı Tepki: {error_msg}")

if __name__ == "__main__":
    test_endpoints()