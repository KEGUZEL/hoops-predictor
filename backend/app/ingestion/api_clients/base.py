from abc import ABC, abstractmethod
from typing import Any, Dict, Mapping

import requests

from app.core.config import get_settings


class RapidApiClient(ABC):
    """
    RapidAPI tabanlı NBA servisleri için basit bir base client.
    """

    def __init__(self, host: str, base_url: str):
        self._settings = get_settings()
        self.host = host
        self.base_url = base_url.rstrip("/")

    @property
    def _headers(self) -> Mapping[str, str]:
        return {
            "x-rapidapi-key": self._settings.rapidapi_key,
            "x-rapidapi-host": self.host,
        }

    def _get(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = requests.get(url, headers=self._headers, params=params, timeout=20)
        resp.raise_for_status()
        return resp.json()

    @abstractmethod
    def ping(self) -> bool:
        """
        Basit bir sağlık kontrolü. Spesifik client'lar override etmelidir.
        """

