from datetime import date
from typing import Any, Dict, List
from loguru import logger

from app.ingestion.api_clients.base import RapidApiClient


class ApiNbaClient(RapidApiClient):
    """
    NBA API Free Data istatistik servisleri için güncellenmiş client.
    """

    def __init__(self) -> None:
        super().__init__(
            host="nba-api-free-data.p.rapidapi.com",
            base_url="https://nba-api-free-data.p.rapidapi.com",
        )

    def ping(self) -> bool:
        try:
            self.get_leagues()
            return True
        except Exception:
            return False

    def get_leagues(self) -> Dict[str, Any]:
        return self._get("/nba-leagues")

    def get_games_by_date(self, d: date) -> List[Dict[str, Any]]:
        date_str = d.strftime("%Y%m%d")
        data = self._get("/nba-scoreboard-by-date", params={"date": date_str})
        
        if isinstance(data, dict):
            inner = data.get("response", {})
            if isinstance(inner, dict):
                return inner.get("Events", []) or []
            if isinstance(inner, list):
                return inner
        return []

    def get_teams_by_division(self, division: str) -> List[Dict[str, Any]]:
        endpoint = f"/nba-{division}-team-list"
        data = self._get(endpoint)
        
        if isinstance(data, dict):
            inner = data.get("response", {})
            if isinstance(inner, dict):
                # API bazen teamList bazen TeamList dönebilir, ikisini de deneyelim
                return inner.get("teamList") or inner.get("TeamList") or []
            if isinstance(inner, list):
                return inner
        return []

    def get_team_roster(self, team_id: str) -> List[Dict[str, Any]]:
        """
        Bir takımın kadrosunu (oyuncularını) döner.
        """
        data = self._get("/nba-player-list", params={"teamid": team_id})
        
        if isinstance(data, dict):
            inner = data.get("response", {})
            if isinstance(inner, dict):
                # DÜZELTME BURADA: 'PlayerList' (Büyük P) ilk sırada
                roster = (
                    inner.get("PlayerList") or 
                    inner.get("playerList") or 
                    inner.get("players") or 
                    inner.get("athletes") or 
                    inner.get("roster") or 
                    []
                )
                
                if roster:
                    return roster
                
                logger.warning(f"ROSTER NOT FOUND! Available keys: {list(inner.keys())}")
                return []
                
            if isinstance(inner, list):
                return inner
        return []

    def get_game_stats(self, game_id: str) -> Dict[str, Any]:
        data = self._get("/nba-game-stats", params={"id": game_id})
        return data if isinstance(data, dict) else {}