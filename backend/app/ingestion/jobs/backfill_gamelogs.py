import time
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.orm import models
from app.ingestion.api_clients.api_nba_client import ApiNbaClient

def run_backfill_gamelogs():
    logger.info("Starting Gamelog Backfill...")
    db: Session = SessionLocal()
    client = ApiNbaClient()
    
    try:
        # Oyuncuları çek (Sadece ID'si düzgün olanlar)
        players = db.query(models.Player).filter(
            ~models.Player.api_player_id.startswith("temp-")
        ).all()
        
        logger.info(f"Found {len(players)} players to process.")

        for player in players:
            # Daha önce stats çekilmişse atla (isteğe bağlı)
            existing_stats = db.query(models.PlayerBoxscore).filter_by(player_id=player.id).count()
            if existing_stats > 5:
                logger.info(f"Skipping {player.name}, already has stats.")
                continue

            logger.info(f"Fetching gamelog for {player.name} ({player.api_player_id})...")
            
            try:
                gamelogs = client.get_player_gamelog(player.api_player_id)
                
                if not gamelogs:
                    logger.warning(f"No gamelogs found for {player.name}")
                    continue
                
                count = 0
                for log in gamelogs:
                    # Gamelog verisinden maç tarihi ve sayıları al
                    # API response yapısına göre bu alanlar değişebilir (örn: 'gameDate', 'pts')
                    # Logları inceleyip burayı düzeltebiliriz.
                    game_id_api = str(log.get("gameId") or log.get("GameId"))
                    date_str = log.get("date") or log.get("Date") # Örn: "2024-01-20"
                    points = int(log.get("points") or log.get("pts") or 0)
                    
                    if not game_id_api: 
                        continue

                    # Maçı bul veya oluştur (Basit versiyon)
                    game = db.query(models.Game).filter_by(api_game_id=game_id_api).first()
                    if not game:
                        try:
                            game_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        except:
                            game_date = datetime.now().date()
                            
                        game = models.Game(
                            api_game_id=game_id_api,
                            date=game_date,
                            home_team_id=player.team_id, # Basitleştirme
                            away_team_id=player.team_id  # Basitleştirme
                        )
                        db.add(game)
                        db.flush()

                    # İstatistiği kaydet
                    box = models.PlayerBoxscore(
                        game_id=game.id,
                        player_id=player.id,
                        points=points,
                        rebounds=int(log.get("rebounds") or log.get("reb") or 0),
                        assists=int(log.get("assists") or log.get("ast") or 0)
                    )
                    db.add(box)
                    count += 1
                
                db.commit()
                logger.info(f" -> Added {count} games for {player.name}")
                time.sleep(2) # Rate limit
                
            except Exception as e:
                logger.error(f"Error for {player.name}: {e}")
                db.rollback()

    except Exception as e:
        logger.error(f"Global error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_backfill_gamelogs()