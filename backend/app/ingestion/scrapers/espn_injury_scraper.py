from datetime import datetime
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup


def scrape_espn_injuries(url: str = "https://www.espn.com/nba/injuries") -> List[Dict[str, Any]]:
    """
    ESPN NBA injuries sayfasından injury verisi çeker.

    Not: ESPN HTML yapısı zamana göre değişebileceği için, burada
    CSS selector'lar örnek olarak verilmiştir. Gerçek projede
    sayfanın güncel yapısına göre selector'ları uyarlamalısın.
    """
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    injuries: List[Dict[str, Any]] = []

    # ÖRNEK: tablo satırlarını bul
    # Gerçekte class isimlerini tarayıcıdan inceleyerek güncelle.
    tables = soup.select("table")
    for table in tables:
        rows = table.select("tbody tr")
        for row in rows:
            cols = [c.get_text(strip=True) for c in row.select("td")]
            if len(cols) < 4:
                continue
            player_name = cols[0]
            team_name = cols[1]
            status = cols[2]
            description = cols[3]

            injuries.append(
                {
                    "player_name": player_name,
                    "team_name": team_name,
                    "status": status,
                    "description": description,
                    "source": "espn",
                    "scraped_at": datetime.utcnow().isoformat(),
                }
            )

    return injuries

