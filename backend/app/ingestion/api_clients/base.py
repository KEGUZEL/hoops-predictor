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
        
        max_retries = 5
        base_wait = 2

        for i in range(max_retries):
            resp = requests.get(url, headers=self._headers, params=params, timeout=20)
            
            if resp.status_code == 429:
                wait_time = base_wait * (2 ** i)
                print(f"⚠️ 429 Rate Limit. Retrying in {wait_time}s... ({i+1}/{max_retries})")
                import time
                time.sleep(wait_time)
                continue
                
            resp.raise_for_status()
            return resp.json()
            
        raise Exception("Max retries exceeded for 429 Rate Limit")

    @abstractmethod
    def ping(self) -> bool:
        """
        Basit bir sağlık kontrolü. Spesifik client'lar override etmelidir.
        """

