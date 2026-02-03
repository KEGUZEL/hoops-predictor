from datetime import timedelta

import pandas as pd
from sqlalchemy.orm import Session

from app.models.orm import models


def compute_player_features(db: Session, window: int = 5) -> pd.DataFrame:
    """
    player_boxscores ve games tablolarından hareketle rolling ortalamalar,
    rest days ve basit bir matchup_difficulty feature'ı hesaplar.

    Output:
        player_features benzeri bir DataFrame döner.
    """
    # Boxscore ve maç verisini çek
    q = (
        db.query(
            models.PlayerBoxscore.id.label("box_id"),
            models.PlayerBoxscore.player_id,
            models.PlayerBoxscore.points,
            models.PlayerBoxscore.rebounds,
            models.PlayerBoxscore.assists,
            models.Game.id.label("game_id"),
            models.Game.date.label("game_date"),
        )
        .join(models.Game, models.Game.id == models.PlayerBoxscore.game_id)
        .order_by(models.PlayerBoxscore.player_id, models.Game.date)
    )
    rows = q.all()
    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(
        [
            {
                "box_id": r.box_id,
                "player_id": r.player_id,
                "game_id": r.game_id,
                "game_date": r.game_date,
                "points": r.points or 0,
                "rebounds": r.rebounds or 0,
                "assists": r.assists or 0,
            }
            for r in rows
        ]
    )

    df["game_date"] = pd.to_datetime(df["game_date"])

    # Rolling ortalamalar
    df = df.sort_values(["player_id", "game_date"])
    df["rolling_pts_5"] = (
        df.groupby("player_id")["points"].rolling(window=window, min_periods=1).mean().reset_index(level=0, drop=True)
    )
    df["rolling_reb_5"] = (
        df.groupby("player_id")["rebounds"].rolling(window=window, min_periods=1).mean().reset_index(level=0, drop=True)
    )
    df["rolling_ast_5"] = (
        df.groupby("player_id")["assists"].rolling(window=window, min_periods=1).mean().reset_index(level=0, drop=True)
    )

    # Rest days
    df["prev_game_date"] = df.groupby("player_id")["game_date"].shift(1)
    df["rest_days"] = (df["game_date"] - df["prev_game_date"]) / pd.Timedelta(days=1)
    df["rest_days"] = df["rest_days"].fillna(3).astype(int)

    # Basit matchup difficulty: lig ortalaması ile kıyaslama (placeholder)
    league_avg_pts = df["points"].mean()
    df["matchup_difficulty_score"] = (league_avg_pts - df["points"]) / (df["points"].std() or 1)

    # Target: bu maçtaki sayı, rolling ortalamanın üstünde mi?
    df["target_above_avg"] = (df["points"] > df["rolling_pts_5"]).astype(int)

    return df[
        [
            "player_id",
            "game_id",
            "rolling_pts_5",
            "rolling_reb_5",
            "rolling_ast_5",
            "matchup_difficulty_score",
            "rest_days",
            "target_above_avg",
        ]
    ]

