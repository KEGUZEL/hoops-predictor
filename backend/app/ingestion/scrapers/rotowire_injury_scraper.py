from datetime import datetime
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup


def scrape_rotowire_injuries(
    url: str = "https://www.rotowire.com/basketball/injury-report.php",
) -> List[Dict[str, Any]]:
    """
    Rotowire NBA injury raporlarını çeker.

    Not: HTML yapısı zamanla değişebilir, selector'ları gerekli
    oldukça güncellemelisin.
    """
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    injuries: List[Dict[str, Any]] = []

    # ÖRNEK selector: gerçek tablo yapısına göre uyarlamalısın.
    rows = soup.select("table tr")
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
                "source": "rotowire",
                "scraped_at": datetime.utcnow().isoformat(),
            }
        )

    return injuries

