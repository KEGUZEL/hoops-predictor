from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class PlayerBase(BaseModel):
    id: int
    name: str
    position: Optional[str] = None

    class Config:
        from_attributes = True


class PlayerHistoryPoint(BaseModel):
    game_date: date
    points: int
    predicted_above_avg: Optional[bool] = None


class PlayerPrediction(BaseModel):
    player: PlayerBase
    game_date: date
    prob_above_avg: float
    prediction_label: str
    rolling_pts_5: float
    season_avg_pts: float  # <--- YENİ EKLENDİ: Sezon Ortalaması
    rest_days: int
    matchup_difficulty_score: float


class PlayerHistoryResponse(BaseModel):
    player: PlayerBase
    history: List[PlayerHistoryPoint]