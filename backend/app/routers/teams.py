from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.orm import models


router = APIRouter()


@router.get("/{team_id}/risk")
def get_team_risk(team_id: int, db: Session = Depends(get_db)):
    """
    Bir takım için basit bir yorgunluk/sakatlık risk skoru hesaplar.

    Şu an için placeholder:
    - Oyuncu sayısı
    - Basit, örnek bir fatigue_score
    """
    team = db.get(models.Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    player_count = len(team.players)

    # Demo amaçlı sabit skorlar (daha sonra Redis/Mongo + gerçek fixture verileriyle zenginleştirilebilir)
    fatigue_score = 30 + player_count  # sadece örnek bir formül

    risk_level = "low"
    if fatigue_score >= 70:
        risk_level = "high"
    elif fatigue_score >= 50:
        risk_level = "medium"

    return {
        "team_id": team_id,
        "team_name": team.name,
        "player_count": player_count,
        "fatigue_score": fatigue_score,
        "risk_level": risk_level,
    }

