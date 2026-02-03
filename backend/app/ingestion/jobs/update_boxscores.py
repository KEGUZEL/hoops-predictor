from datetime import date, timedelta
from loguru import logger
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.ingestion.api_clients.api_nba_client import ApiNbaClient
from app.models.orm import models


def _get_or_create_team_placeholder(db: Session, team_name: str) -> models.Team:
    """
    Takım ID'si API'de açıkça yoksa isminden bulmaya çalışır veya placeholder oluşturur.
    """
    # İsimden bulmaya çalış (Basit eşleştirme)
    team = db.query(models.Team).filter(models.Team.name.ilike(f"%{team_name}%")).first()
    if team:
        return team
    
    # Yoksa geçici oluştur
    slug = team_name.lower().replace(" ", "-")
    team = models.Team(api_team_id=f"temp-{slug}", name=team_name, abbreviation=team_name[:3].upper())
    db.add(team)
    db.flush()
    return team

def run_update_boxscores(target_date: date | None = None) -> None:
    target_date = target_date or (date.today() - timedelta(days=1))
    logger.info(f"Updating boxscores for {target_date}")

    client = ApiNbaClient()
    games_data = client.get_games_by_date(target_date)
    
    if not games_data:
        logger.warning("No games found for this date.")
        return

    db: Session = SessionLocal()
    try:
        for g in games_data:
            # --- YENİ RESPONSE PARSING ---
            # Gelen veri: { "id": "401705165", "name": "Dallas Mavericks at Charlotte Hornets", ... }
            api_game_id = str(g.get("id"))
            game_name = g.get("name", "Unknown vs Unknown")
            
            # İsimden takımları ayıkla: "Dallas Mavericks at Charlotte Hornets"
            if " at " in game_name:
                away_name, home_name = game_name.split(" at ")
            elif " vs " in game_name:
                home_name, away_name = game_name.split(" vs ")
            else:
                logger.warning(f"Could not parse team names from: {game_name}")
                continue

            # Takımları bul veya oluştur
            home_team = _get_or_create_team_placeholder(db, home_name)
            away_team = _get_or_create_team_placeholder(db, away_name)

            # Maçı kaydet
            game = db.query(models.Game).filter_by(api_game_id=api_game_id).first()
            if not game:
                game = models.Game(
                    api_game_id=api_game_id,
                    season=target_date.year,
                    date=target_date,
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    home_score=0, # Skor bilgisi detayda olabilir, şimdilik 0
                    away_score=0
                )
                db.add(game)
                db.flush()
            
            logger.info(f"Processed Game: {game_name} (ID: {api_game_id})")
            
            # --- DETAY / BOXSCORE ---
            # Not: Ücretsiz planda boxscore detayı vermeyebilir. 
            # Eğer hata verirse burayı try-except içine al.
            try:
                # Buraya detay çekme kodu gelecek (şimdilik pass geçiyoruz çünkü endpoint belirsiz)
                pass 
            except Exception as e:
                logger.error(f"Could not fetch stats for game {api_game_id}: {e}")

        db.commit()
        logger.info("Boxscores update completed.")
    except Exception as exc:
        db.rollback()
        logger.exception(f"Boxscores update failed: {exc}")
    finally:
        db.close()

if __name__ == "__main__":
    run_update_boxscores()