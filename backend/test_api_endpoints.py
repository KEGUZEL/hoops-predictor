"""
NBA API Free Data endpoint'lerini test etmek için script.
"""
from app.ingestion.api_clients.base import RapidApiClient
from app.core.config import get_settings
import json


def test_endpoints():
    from app.ingestion.api_clients.api_nba_client import ApiNbaClient
    
    client = ApiNbaClient()
    
    # Test edilecek endpoint'ler
    endpoints = [
        "/nba-leagues",
        "/nba-league-info",
        "/nba-sport-info",
        "/nba-scoreboard",
        "/nba-player-stats",
        "/nba-game-details",
        "/nba-team-list",
        "/nba-team-info",
        "/nba-standings",
    ]
    
    print("Testing NBA API Free Data endpoints...")
    print("=" * 60)
    
    for endpoint in endpoints:
        try:
            data = client._get(endpoint)
            print(f"✅ {endpoint}")
            print(f"   Response type: {type(data)}")
            if isinstance(data, dict):
                print(f"   Keys: {list(data.keys())[:5]}")
            print()
        except Exception as e:
            print(f"❌ {endpoint}")
            print(f"   Error: {str(e)[:100]}")
            print()


if __name__ == "__main__":
    test_endpoints()
