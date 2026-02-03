from datetime import date
from typing import Any, Dict, List

from app.ingestion.api_clients.base import RapidApiClient


class ApiNbaClient(RapidApiClient):
    """
    NBA API Free Data istatistik servisleri için client.

    Referans: https://rapidapi.com/api-nba-free-data
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
        """
        NBA ligini döner.
        """
        data = self._get("/nba-leagues")
        return data

    def get_games_by_date(self, d: date) -> List[Dict[str, Any]]:
        """
        Belirli bir tarihteki maçları döner.
        Format: YYYYMMDD (örn: 20240301)
        """
        date_str = d.strftime("%Y%m%d")
        data = self._get(f"/nba-schedule", params={"date": date_str})
        # Response format: {"events": [...]}
        if isinstance(data, dict):
            return data.get("events", [])
        return []

    def get_game_stats(self, game_id: str) -> Dict[str, Any]:
        """
        Bir maç için detaylı istatistikler.
        """
        data = self._get(f"/nba-game-stats", params={"id": game_id})
        return data if isinstance(data, dict) else {}

    def get_team_roster(self, team_id: str) -> List[Dict[str, Any]]:
        """
        Bir takımın kadrosunu döner.
        """
        data = self._get(f"/nba-team-roster", params={"id": team_id})
        if isinstance(data, dict):
            return data.get("athletes", [])
        return []


