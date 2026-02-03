from datetime import date
from typing import Any, Dict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.orm import models


def predict_player_next_game(
    db: Session,
    player_id: int,
    game_date: date | None = None,
) -> Dict[str, Any]:
    """
    Oyuncunun bir sonraki maçı için tahmin ve istatistik döner.
    """
    # 1. Gerçek Sezon Ortalamasını Hesapla
    season_avg = (
        db.query(func.avg(models.PlayerBoxscore.points))
        .filter(models.PlayerBoxscore.player_id == player_id)
        .scalar()
    )
    # Veri yoksa 0.0, varsa float çevir
    season_avg_pts = float(season_avg) if season_avg is not None else 0.0

    # 2. ML Özelliklerini Çek
    features = (
        db.query(models.PlayerFeatures)
        .filter(models.PlayerFeatures.player_id == player_id)
        .order_by(models.PlayerFeatures.id.desc())
        .first()
    )

    today = game_date or date.today()

    if features:
        rolling_pts_5 = features.rolling_pts_5 or season_avg_pts
        rest_days = features.rest_days or 2
        matchup_difficulty_score = features.matchup_difficulty_score or 0.0
    else:
        rolling_pts_5 = season_avg_pts
        rest_days = 2
        matchup_difficulty_score = 0.0

    # Basit Tahmin Mantığı
    base_prob = 0.5
    if rolling_pts_5 > season_avg_pts:
        base_prob += 0.1
    if rest_days <= 1:
        base_prob -= 0.1
        
    prob_above_avg = max(0.05, min(0.95, base_prob))
    prediction_label = "Above Average" if prob_above_avg >= 0.5 else "Below Average"

    # BURADAKİ return SÖZLÜĞÜ ARTIK 'season_avg_pts' İÇERİYOR
    return {
        "game_date": today,
        "prob_above_avg": prob_above_avg,
        "prediction_label": prediction_label,
        "rolling_pts_5": rolling_pts_5,
        "season_avg_pts": season_avg_pts,  # <--- İşte eksik parça buydu!
        "rest_days": rest_days,
        "matchup_difficulty_score": matchup_difficulty_score,
    }