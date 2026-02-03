from datetime import date
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models.orm import models


def predict_player_next_game(
    db: Session,
    player_id: int,
    game_date: date | None = None,
) -> Dict[str, Any]:
    """
    Basit bir placeholder prediction fonksiyonu.

    Gerçek senaryoda:
    - player_features tablosundan rolling ortalamalar, rest days ve matchup zorluk skorları çekilir.
    - Eğitimli ML modeli (ör. XGBoost) yüklenir ve özellikler üzerinden tahmin yapılır.

    Şimdilik demo amaçlı sabit bir olasılık ve örnek feature değerleri döndürür.
    """
    # Örnek: Son feature kaydını al (varsa)
    features = (
        db.query(models.PlayerFeatures)
        .filter(models.PlayerFeatures.player_id == player_id)
        .order_by(models.PlayerFeatures.id.desc())
        .first()
    )

    today = game_date or date.today()

    if features:
        rolling_pts_5 = features.rolling_pts_5 or 0.0
        rest_days = features.rest_days or 2
        matchup_difficulty_score = features.matchup_difficulty_score or 0.0
    else:
        # Eğer feature yoksa, güvenli default değerler
        rolling_pts_5 = 15.0
        rest_days = 2
        matchup_difficulty_score = 0.0

    # Placeholder: basit bir kural tabanlı olasılık
    base_prob = 0.5
    if rest_days <= 1:
        base_prob -= 0.1
    if matchup_difficulty_score > 0:
        base_prob -= 0.1
    if rolling_pts_5 > 20:
        base_prob += 0.1

    prob_above_avg = max(0.05, min(0.95, base_prob))
    prediction_label = "Above Average" if prob_above_avg >= 0.5 else "Below Average"

    return {
        "game_date": today,
        "prob_above_avg": prob_above_avg,
        "prediction_label": prediction_label,
        "rolling_pts_5": rolling_pts_5,
        "rest_days": rest_days,
        "matchup_difficulty_score": matchup_difficulty_score,
    }

