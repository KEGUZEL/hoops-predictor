from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.orm import models
from app.models.schemas.players import (
    PlayerPrediction,
    PlayerHistoryResponse,
    PlayerBase,
    PlayerHistoryPoint,
)
from app.ml.predictor import predict_player_next_game


router = APIRouter()

@router.get("/", response_model=List[PlayerBase])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Tüm oyuncuların listesini döner. Frontend'de seçim kutusu (dropdown) için kullanılır.
    """
    players = db.query(models.Player).offset(skip).limit(limit).all()
    return players

@router.get("/{player_id}/prediction", response_model=PlayerPrediction)
def get_player_prediction(
    player_id: int,
    game_date: date | None = None,
    db: Session = Depends(get_db),
) -> Any:
    """
    Bir oyuncunun bir sonraki maçında kendi ortalamasının üstüne çıkıp çıkmayacağına dair tahmini döner.
    Şu an için ML modeli basit bir placeholder olarak uygulanmıştır.
    """
    player = db.get(models.Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    result = predict_player_next_game(db, player_id=player_id, game_date=game_date)

    return PlayerPrediction(
        player=PlayerBase.from_orm(player),
        game_date=result["game_date"],
        prob_above_avg=result["prob_above_avg"],
        prediction_label=result["prediction_label"],
        rolling_pts_5=result["rolling_pts_5"],
        rest_days=result["rest_days"],
        matchup_difficulty_score=result["matchup_difficulty_score"],
    )


@router.get("/{player_id}/history", response_model=PlayerHistoryResponse)
def get_player_history(
    player_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
) -> Any:
    """
    Frontend grafiği için oyuncunun son X maçtaki performansını döner.
    Şimdilik basit bir sorgu ve örnek şema ile yapılandırılmıştır.
    """
    player = db.get(models.Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Basitleştirilmiş örnek: Son maçları tarih sırasına göre çek
    q = (
        db.query(models.Game, models.PlayerBoxscore)
        .join(models.PlayerBoxscore, models.Game.id == models.PlayerBoxscore.game_id)
        .filter(models.PlayerBoxscore.player_id == player_id)
        .order_by(models.Game.date.desc())
        .limit(limit)
    )

    history = [
        PlayerHistoryPoint(
            game_date=game.date,
            points=box.points or 0,
            predicted_above_avg=None,  # İleride gerçek tahmin sonuçlarıyla doldurulabilir
        )
        for game, box in q.all()
    ]

    return PlayerHistoryResponse(
        player=PlayerBase.from_orm(player),
        history=list(reversed(history)),
    )

