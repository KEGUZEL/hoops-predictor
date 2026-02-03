from datetime import date, timedelta

from loguru import logger
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.ingestion.api_clients.api_nba_client import ApiNbaClient
from app.models.orm import models


def _get_or_create_team(db: Session, api_team_id: str, name: str, abbreviation: str) -> models.Team:
    team = db.query(models.Team).filter_by(api_team_id=api_team_id).first()
    if team:
        return team
    team = models.Team(api_team_id=api_team_id, name=name, abbreviation=abbreviation)
    db.add(team)
    db.flush()
    return team


def _get_or_create_player(db: Session, api_player_id: str, name: str, team: models.Team) -> models.Player:
    player = db.query(models.Player).filter_by(api_player_id=api_player_id).first()
    if player:
        return player
    player = models.Player(api_player_id=api_player_id, name=name, team=team)
    db.add(player)
    db.flush()
    return player


def run_update_boxscores(target_date: date | None = None) -> None:
    """
    API-NBA üzerinden belirli bir tarihteki maçları ve boxscore'ları alıp
    PostgreSQL veritabanına yazar.

    Not: JSON şemasını RapidAPI playground'dan inceleyerek mapping kısmını
    gerektiğinde güncelleyebilirsin.
    """
    target_date = target_date or (date.today() - timedelta(days=1))
    logger.info(f"Updating boxscores for {target_date}")

    client = ApiNbaClient()
    games_data = client.get_games_by_date(target_date)

    db: Session = SessionLocal()
    try:
        for g in games_data:
            # Buradaki alan isimleri, API-NBA response yapısına göre örneklenmiştir.
            api_game_id = str(g.get("id") or g.get("gameId"))
            if not api_game_id:
                continue

            # Takım bilgileri (örnek, dokümantasyona göre güncelle)
            home_team_info = g.get("teams", {}).get("home", {})
            away_team_info = g.get("teams", {}).get("visitors", {})

            home_team = _get_or_create_team(
                db,
                api_team_id=str(home_team_info.get("id")),
                name=home_team_info.get("name", "Home"),
                abbreviation=home_team_info.get("nickname", "H"),
            )
            away_team = _get_or_create_team(
                db,
                api_team_id=str(away_team_info.get("id")),
                name=away_team_info.get("name", "Away"),
                abbreviation=away_team_info.get("nickname", "A"),
            )

            game = (
                db.query(models.Game)
                .filter_by(api_game_id=api_game_id)
                .first()
            )
            if not game:
                game = models.Game(
                    api_game_id=api_game_id,
                    season=g.get("season") or target_date.year,
                    date=target_date,
                    home_team_id=home_team.id,
                    away_team_id=away_team.id,
                    home_score=g.get("scores", {})
                    .get("home", {})
                    .get("points"),
                    away_score=g.get("scores", {})
                    .get("visitors", {})
                    .get("points"),
                )
                db.add(game)
                db.flush()

            # Boxscore istatistikleri
            stats_data = client.get_game_stats(int(api_game_id))
            for stat in stats_data:
                player_info = stat.get("player", {})
                api_player_id = str(player_info.get("id"))
                if not api_player_id:
                    continue
                player_name = player_info.get("name") or player_info.get("firstname", "")
                player = _get_or_create_player(db, api_player_id=api_player_id, name=player_name, team=home_team)

                stats = stat.get("statistics", {})
                box = models.PlayerBoxscore(
                    game_id=game.id,
                    player_id=player.id,
                    minutes=float(stats.get("min") or 0) if stats.get("min") else None,
                    points=int(stats.get("points") or 0),
                    rebounds=int(stats.get("totReb") or 0),
                    assists=int(stats.get("assists") or 0),
                    fgm=int(stats.get("fgm") or 0),
                    fga=int(stats.get("fga") or 0),
                    ftm=int(stats.get("ftm") or 0),
                    fta=int(stats.get("fta") or 0),
                    tpm=int(stats.get("tpm") or 0),
                    tpa=int(stats.get("tpa") or 0),
                    turnovers=int(stats.get("turnovers") or 0),
                    plus_minus=int(stats.get("plusMinus") or 0)
                    if stats.get("plusMinus") is not None
                    else None,
                )
                db.add(box)

        db.commit()
        logger.info("Boxscores update completed.")
    except Exception as exc:
        db.rollback()
        logger.exception(f"Boxscores update failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_update_boxscores()

