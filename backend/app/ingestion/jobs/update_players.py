import time
from loguru import logger
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.orm import models
from app.ingestion.api_clients.api_nba_client import ApiNbaClient

def run_update_players():
    logger.info("Starting player roster update (Smart Mode)...")
    
    db: Session = SessionLocal()
    client = ApiNbaClient()
    
    try:
        teams = db.query(models.Team).all()
        logger.info(f"Found {len(teams)} teams in database.")
        
        for team in teams:
            # --- YENİ KONTROL ---
            # Eğer takımın zaten oyuncusu varsa API'ye gitme, pas geç.
            player_count = db.query(models.Player).filter_by(team_id=team.id).count()
            if player_count > 5:  # 5'ten fazla oyuncusu varsa tamamdır
                logger.info(f"Skipping {team.name}, already has {player_count} players.")
                continue
            
            # Temp ID kontrolü
            if str(team.api_team_id).startswith("temp-"):
                logger.warning(f"Skipping temp team: {team.name}")
                continue

            logger.info(f"Fetching roster for {team.name} (API ID: {team.api_team_id})...")

            try:
                # 2. Takım ID'si ile oyuncu listesini çek
                roster_data = client.get_team_roster(team.api_team_id)
                
                if not roster_data:
                    logger.warning(f"No players found for {team.name}")
                    continue

                count = 0
                for p_data in roster_data:
                    api_player_id = str(p_data.get("id"))
                    
                    first = p_data.get("firstName") or p_data.get("firstname") or ""
                    last = p_data.get("lastName") or p_data.get("lastname") or ""
                    name = f"{first} {last}".strip()
                    if not name:
                        name = p_data.get("name") or "Unknown"

                    if not api_player_id:
                        continue
                        
                    player = db.query(models.Player).filter_by(api_player_id=api_player_id).first()
                    
                    pos = None
                    leagues = p_data.get("leagues", {})
                    if isinstance(leagues, dict):
                        standard = leagues.get("standard", {})
                        if isinstance(standard, dict):
                            pos = standard.get("pos")

                    if not player:
                        player = models.Player(
                            api_player_id=api_player_id,
                            name=name,
                            team_id=team.id,
                            position=pos
                        )
                        db.add(player)
                        count += 1
                    else:
                        player.team_id = team.id
                        if pos:
                            player.position = pos
                
                db.commit()
                logger.info(f" -> Processed {len(roster_data)} players, New: {count}")
                
                # HIZ LİMİTİ KORUMASI: 2 saniye bekle
                time.sleep(2) 
                
            except Exception as e:
                # 429 hatası alırsak loglayıp çıkalım, zorlamayalım
                if "429" in str(e):
                    logger.error("API Rate Limit Hit (429)! Stopping for now.")
                    break
                logger.error(f"Failed to fetch roster for {team.name}: {e}")
                db.rollback()

    except Exception as e:
        logger.error(f"Global error: {e}")
    finally:
        db.close()
        logger.info("Player update job finished.")

if __name__ == "__main__":
    run_update_players()