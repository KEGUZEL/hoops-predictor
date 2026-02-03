from loguru import logger
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.ml.features import compute_player_features
from app.models.orm import models


def run_recompute_features() -> None:
    """
    player_boxscores ve games verisini kullanarak player_features tablosunu günceller.
    """
    logger.info("Recomputing player features...")
    db: Session = SessionLocal()
    try:
        df = compute_player_features(db)
        if df.empty:
            logger.info("No boxscore data found, skipping feature computation.")
            return

        # Mevcut feature'ları temizleyebilirsin (basit strateji)
        db.query(models.PlayerFeatures).delete()
        db.commit()

        # Yeni feature satırlarını ekle
        for row in df.to_dict(orient="records"):
            feat = models.PlayerFeatures(
                player_id=row["player_id"],
                game_id=row["game_id"],
                rolling_pts_5=row["rolling_pts_5"],
                rolling_reb_5=row["rolling_reb_5"],
                rolling_ast_5=row["rolling_ast_5"],
                matchup_difficulty_score=row["matchup_difficulty_score"],
                rest_days=row["rest_days"],
                target_above_avg=bool(row["target_above_avg"]),
            )
            db.add(feat)

        db.commit()
        logger.info(f"Inserted {len(df)} feature rows.")
    except Exception as exc:
        db.rollback()
        logger.exception(f"Feature recompute failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_recompute_features()

