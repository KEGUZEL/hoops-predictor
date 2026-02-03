from datetime import date
from typing import Any, Dict, List

from app.ingestion.api_clients.base import RapidApiClient


class InjuryApiClient(RapidApiClient):
    """
    NBA Injury Data servisi için client.

    Referans: https://rapidapi.com/DillonMarks1/api/nba-injury-data
    """

    def __init__(self) -> None:
        super().__init__(
            host="nba-injury-data.p.rapidapi.com",
            base_url="https://nba-injury-data.p.rapidapi.com",
        )

    def ping(self) -> bool:
        try:
            self.get_injuries_by_date(date.today())
            return True
        except Exception:
            return False

    def get_injuries_by_date(self, d: date) -> List[Dict[str, Any]]:
        """
        Belirli tarih için injury raporları.
        Endpoint ve parametreler, RapidAPI playground dokümantasyonuna göre uyarlanmalıdır.
        """
        data = self._get("/injuries", params={"date": d.isoformat()})
        # Dönen JSON şemasına göre burada normalizasyon yapabilirsin.
        return data if isinstance(data, list) else data.get("response", [])

