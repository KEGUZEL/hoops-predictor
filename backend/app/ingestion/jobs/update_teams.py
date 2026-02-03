import time
from loguru import logger
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.orm import models
from app.ingestion.api_clients.api_nba_client import ApiNbaClient

# API'deki 6 bölgenin tam listesi
DIVISIONS = [
    "atlantic",   # Boston, Nets, Knicks, 76ers, Raptors
    "central",    # Bulls, Cavs, Pistons, Pacers, Bucks
    "southeast",  # Hawks, Hornets, Heat, Magic, Wizards
    "northwest",  # Nuggets, Wolves, Thunder, Blazers, Jazz
    "pacific",    # Warriors, Clippers, Lakers, Suns, Kings
    "southwest"   # Mavs, Rockets, Grizzlies, Pelicans, Spurs
]

def run_update_teams():
    logger.info("Starting team ID update process via Divisions...")
    db: Session = SessionLocal()
    client = ApiNbaClient()
    
    try:
        updated_count = 0
        created_count = 0
        
        for division in DIVISIONS:
            logger.info(f"Fetching teams for division: {division}...")
            try:
                # 1. API'den o bölgenin takımlarını çek
                teams_data = client.get_teams_by_division(division)
                
                if not teams_data:
                    logger.warning(f"No teams found for division: {division}")
                    continue

                for t_data in teams_data:
                    # Kanıt: image_e1dda2.png -> {"id": "2", "name": "Boston Celtics", "abbrev": "bos"}
                    real_id = str(t_data.get("id"))
                    name = t_data.get("name")
                    abbrev = t_data.get("abbrev") or t_data.get("shortName")
                    
                    if not real_id or not name:
                        continue

                    # 2. Veritabanında bu isimle takım var mı? (temp ID ile oluşturduğumuz)
                    existing_team = db.query(models.Team).filter(
                        models.Team.name.ilike(name)
                    ).first()

                    if existing_team:
                        # Eğer ID'si zaten doğruysa geç
                        if existing_team.api_team_id == real_id:
                            continue
                            
                        # ID'yi güncelle ("temp-dallas..." -> "13")
                        logger.info(f"Updating ID for {name}: {existing_team.api_team_id} -> {real_id}")
                        existing_team.api_team_id = real_id
                        existing_team.abbreviation = abbrev or existing_team.abbreviation
                        existing_team.division = division
                        updated_count += 1
                    else:
                        # Takım hiç yoksa (maç verisinde çıkmamışsa) sıfırdan oluştur
                        logger.info(f"Creating new team: {name} ({real_id})")
                        new_team = models.Team(
                            api_team_id=real_id,
                            name=name,
                            abbreviation=abbrev or "N/A",
                            division=division
                        )
                        db.add(new_team)
                        created_count += 1
                
                db.commit()
                time.sleep(1) # API'yi yormamak için bekleme
                
            except Exception as e:
                logger.error(f"Error processing division {division}: {e}")
                
        logger.info(f"Team update finished. Updated: {updated_count}, Created: {created_count}")

    except Exception as e:
        logger.error(f"Global error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_update_teams()