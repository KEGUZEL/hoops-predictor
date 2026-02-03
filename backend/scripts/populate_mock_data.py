"""
Geniş kapsamlı mock NBA verisi oluşturur.
10+ takım, 50+ oyuncu, 30+ maç ve detaylı istatistikler içerir.
"""
from datetime import date, timedelta
import random
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.orm import models


# NBA Takımları (Gerçek takımlar)
TEAMS_DATA = [
    {"api_team_id": "1", "name": "Los Angeles Lakers", "abbreviation": "LAL", "conference": "West", "division": "Pacific"},
    {"api_team_id": "2", "name": "Boston Celtics", "abbreviation": "BOS", "conference": "East", "division": "Atlantic"},
    {"api_team_id": "3", "name": "Golden State Warriors", "abbreviation": "GSW", "conference": "West", "division": "Pacific"},
    {"api_team_id": "4", "name": "Miami Heat", "abbreviation": "MIA", "conference": "East", "division": "Southeast"},
    {"api_team_id": "5", "name": "Chicago Bulls", "abbreviation": "CHI", "conference": "East", "division": "Central"},
    {"api_team_id": "6", "name": "Dallas Mavericks", "abbreviation": "DAL", "conference": "West", "division": "Southwest"},
    {"api_team_id": "7", "name": "Brooklyn Nets", "abbreviation": "BKN", "conference": "East", "division": "Atlantic"},
    {"api_team_id": "8", "name": "Phoenix Suns", "abbreviation": "PHX", "conference": "West", "division": "Pacific"},
    {"api_team_id": "9", "name": "Milwaukee Bucks", "abbreviation": "MIL", "conference": "East", "division": "Central"},
    {"api_team_id": "10", "name": "Denver Nuggets", "abbreviation": "DEN", "conference": "West", "division": "Northwest"},
    {"api_team_id": "11", "name": "Philadelphia 76ers", "abbreviation": "PHI", "conference": "East", "division": "Atlantic"},
    {"api_team_id": "12", "name": "Memphis Grizzlies", "abbreviation": "MEM", "conference": "West", "division": "Southwest"},
]

# Oyuncular (Her takım için 5-6 oyuncu)
PLAYERS_DATA = [
    # Lakers
    {"api_player_id": "1", "team_abbr": "LAL", "name": "LeBron James", "position": "SF"},
    {"api_player_id": "2", "team_abbr": "LAL", "name": "Anthony Davis", "position": "PF"},
    {"api_player_id": "3", "team_abbr": "LAL", "name": "D'Angelo Russell", "position": "PG"},
    {"api_player_id": "4", "team_abbr": "LAL", "name": "Austin Reaves", "position": "SG"},
    {"api_player_id": "5", "team_abbr": "LAL", "name": "Rui Hachimura", "position": "SF"},
    
    # Celtics
    {"api_player_id": "6", "team_abbr": "BOS", "name": "Jayson Tatum", "position": "SF"},
    {"api_player_id": "7", "team_abbr": "BOS", "name": "Jaylen Brown", "position": "SG"},
    {"api_player_id": "8", "team_abbr": "BOS", "name": "Kristaps Porzingis", "position": "C"},
    {"api_player_id": "9", "team_abbr": "BOS", "name": "Derrick White", "position": "PG"},
    {"api_player_id": "10", "team_abbr": "BOS", "name": "Jrue Holiday", "position": "SG"},
    
    # Warriors
    {"api_player_id": "11", "team_abbr": "GSW", "name": "Stephen Curry", "position": "PG"},
    {"api_player_id": "12", "team_abbr": "GSW", "name": "Klay Thompson", "position": "SG"},
    {"api_player_id": "13", "team_abbr": "GSW", "name": "Draymond Green", "position": "PF"},
    {"api_player_id": "14", "team_abbr": "GSW", "name": "Andrew Wiggins", "position": "SF"},
    {"api_player_id": "15", "team_abbr": "GSW", "name": "Chris Paul", "position": "PG"},
    
    # Heat
    {"api_player_id": "16", "team_abbr": "MIA", "name": "Jimmy Butler", "position": "SF"},
    {"api_player_id": "17", "team_abbr": "MIA", "name": "Bam Adebayo", "position": "C"},
    {"api_player_id": "18", "team_abbr": "MIA", "name": "Tyler Herro", "position": "SG"},
    {"api_player_id": "19", "team_abbr": "MIA", "name": "Kyle Lowry", "position": "PG"},
    {"api_player_id": "20", "team_abbr": "MIA", "name": "Duncan Robinson", "position": "SG"},
    
    # Bulls
    {"api_player_id": "21", "team_abbr": "CHI", "name": "DeMar DeRozan", "position": "SF"},
    {"api_player_id": "22", "team_abbr": "CHI", "name": "Zach LaVine", "position": "SG"},
    {"api_player_id": "23", "team_abbr": "CHI", "name": "Nikola Vucevic", "position": "C"},
    {"api_player_id": "24", "team_abbr": "CHI", "name": "Coby White", "position": "PG"},
    {"api_player_id": "25", "team_abbr": "CHI", "name": "Alex Caruso", "position": "SG"},
    
    # Mavericks
    {"api_player_id": "26", "team_abbr": "DAL", "name": "Luka Doncic", "position": "PG"},
    {"api_player_id": "27", "team_abbr": "DAL", "name": "Kyrie Irving", "position": "SG"},
    {"api_player_id": "28", "team_abbr": "DAL", "name": "Dereck Lively II", "position": "C"},
    {"api_player_id": "29", "team_abbr": "DAL", "name": "Josh Green", "position": "SG"},
    {"api_player_id": "30", "team_abbr": "DAL", "name": "Grant Williams", "position": "PF"},
    
    # Nets
    {"api_player_id": "31", "team_abbr": "BKN", "name": "Mikal Bridges", "position": "SF"},
    {"api_player_id": "32", "team_abbr": "BKN", "name": "Cam Thomas", "position": "SG"},
    {"api_player_id": "33", "team_abbr": "BKN", "name": "Nic Claxton", "position": "C"},
    {"api_player_id": "34", "team_abbr": "BKN", "name": "Spencer Dinwiddie", "position": "PG"},
    {"api_player_id": "35", "team_abbr": "BKN", "name": "Dorian Finney-Smith", "position": "PF"},
    
    # Suns
    {"api_player_id": "36", "team_abbr": "PHX", "name": "Kevin Durant", "position": "SF"},
    {"api_player_id": "37", "team_abbr": "PHX", "name": "Devin Booker", "position": "SG"},
    {"api_player_id": "38", "team_abbr": "PHX", "name": "Bradley Beal", "position": "SG"},
    {"api_player_id": "39", "team_abbr": "PHX", "name": "Jusuf Nurkic", "position": "C"},
    {"api_player_id": "40", "team_abbr": "PHX", "name": "Grayson Allen", "position": "SG"},
    
    # Bucks
    {"api_player_id": "41", "team_abbr": "MIL", "name": "Giannis Antetokounmpo", "position": "PF"},
    {"api_player_id": "42", "team_abbr": "MIL", "name": "Damian Lillard", "position": "PG"},
    {"api_player_id": "43", "team_abbr": "MIL", "name": "Khris Middleton", "position": "SF"},
    {"api_player_id": "44", "team_abbr": "MIL", "name": "Brook Lopez", "position": "C"},
    {"api_player_id": "45", "team_abbr": "MIL", "name": "Bobby Portis", "position": "PF"},
    
    # Nuggets
    {"api_player_id": "46", "team_abbr": "DEN", "name": "Nikola Jokic", "position": "C"},
    {"api_player_id": "47", "team_abbr": "DEN", "name": "Jamal Murray", "position": "PG"},
    {"api_player_id": "48", "team_abbr": "DEN", "name": "Michael Porter Jr.", "position": "SF"},
    {"api_player_id": "49", "team_abbr": "DEN", "name": "Aaron Gordon", "position": "PF"},
    {"api_player_id": "50", "team_abbr": "DEN", "name": "Kentavious Caldwell-Pope", "position": "SG"},
    
    # 76ers
    {"api_player_id": "51", "team_abbr": "PHI", "name": "Joel Embiid", "position": "C"},
    {"api_player_id": "52", "team_abbr": "PHI", "name": "Tyrese Maxey", "position": "PG"},
    {"api_player_id": "53", "team_abbr": "PHI", "name": "Tobias Harris", "position": "PF"},
    {"api_player_id": "54", "team_abbr": "PHI", "name": "De'Anthony Melton", "position": "SG"},
    {"api_player_id": "55", "team_abbr": "PHI", "name": "Kelly Oubre Jr.", "position": "SF"},
    
    # Grizzlies
    {"api_player_id": "56", "team_abbr": "MEM", "name": "Ja Morant", "position": "PG"},
    {"api_player_id": "57", "team_abbr": "MEM", "name": "Desmond Bane", "position": "SG"},
    {"api_player_id": "58", "team_abbr": "MEM", "name": "Jaren Jackson Jr.", "position": "PF"},
    {"api_player_id": "59", "team_abbr": "MEM", "name": "Marcus Smart", "position": "PG"},
    {"api_player_id": "60", "team_abbr": "MEM", "name": "Steven Adams", "position": "C"},
]


def generate_player_stats(player_name: str, is_star: bool = False) -> dict:
    """Oyuncu için gerçekçi istatistikler üretir."""
    if is_star:
        # Yıldız oyuncular için yüksek istatistikler
        return {
            "minutes": round(random.uniform(32, 38), 1),
            "points": random.randint(22, 35),
            "rebounds": random.randint(5, 12),
            "assists": random.randint(4, 10),
            "fgm": random.randint(8, 14),
            "fga": random.randint(16, 24),
            "ftm": random.randint(4, 10),
            "fta": random.randint(5, 12),
            "tpm": random.randint(2, 6),
            "tpa": random.randint(5, 12),
            "turnovers": random.randint(1, 4),
            "plus_minus": random.randint(-5, 15),
        }
    else:
        # Normal oyuncular için orta seviye istatistikler
        return {
            "minutes": round(random.uniform(18, 28), 1),
            "points": random.randint(8, 18),
            "rebounds": random.randint(2, 7),
            "assists": random.randint(1, 5),
            "fgm": random.randint(3, 7),
            "fga": random.randint(7, 14),
            "ftm": random.randint(1, 4),
            "fta": random.randint(1, 5),
            "tpm": random.randint(0, 3),
            "tpa": random.randint(1, 6),
            "turnovers": random.randint(0, 3),
            "plus_minus": random.randint(-8, 8),
        }


def populate_mock_data():
    """Veritabanını geniş mock veri ile doldurur."""
    db: Session = SessionLocal()
    
    try:
        print("🏀 Mock NBA verisi oluşturuluyor...")
        print("=" * 60)
        
        # 1. Takımları ekle
        print("\n📊 Takımlar ekleniyor...")
        teams_map = {}
        for team_data in TEAMS_DATA:
            team = models.Team(**team_data)
            db.add(team)
            db.flush()
            teams_map[team_data["abbreviation"]] = team
            print(f"  ✅ {team.name} ({team.abbreviation})")
        
        db.commit()
        print(f"\n✅ {len(TEAMS_DATA)} takım eklendi!")
        
        # 2. Oyuncuları ekle
        print("\n👥 Oyuncular ekleniyor...")
        players_map = {}
        star_players = ["LeBron James", "Stephen Curry", "Giannis Antetokounmpo", 
                       "Nikola Jokic", "Luka Doncic", "Joel Embiid", "Kevin Durant",
                       "Jayson Tatum", "Damian Lillard", "Anthony Davis"]
        
        for player_data in PLAYERS_DATA:
            team = teams_map[player_data["team_abbr"]]
            player = models.Player(
                api_player_id=player_data["api_player_id"],
                team_id=team.id,
                name=player_data["name"],
                position=player_data["position"]
            )
            db.add(player)
            db.flush()
            players_map[player_data["name"]] = player
            print(f"  ✅ {player.name} ({player.position}) - {team.abbreviation}")
        
        db.commit()
        print(f"\n✅ {len(PLAYERS_DATA)} oyuncu eklendi!")
        
        # 3. Maçları ve istatistikleri ekle
        print("\n🏆 Maçlar ve istatistikler oluşturuluyor...")
        
        game_count = 0
        start_date = date.today() - timedelta(days=45)
        
        # 40 maç oluştur
        for i in range(40):
            game_date = start_date + timedelta(days=i)
            
            # Rastgele iki takım seç
            home_team, away_team = random.sample(list(teams_map.values()), 2)
            
            # Maç skoru oluştur (gerçekçi skorlar)
            home_score = random.randint(95, 125)
            away_score = random.randint(95, 125)
            
            # Maç oluştur
            game = models.Game(
                api_game_id=f"mock_game_{i+1}",
                season=2024,
                date=game_date,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                home_score=home_score,
                away_score=away_score
            )
            db.add(game)
            db.flush()
            game_count += 1
            
            # Her takımdan 5 oyuncu seç ve istatistik ekle
            home_players = [p for p in players_map.values() if p.team_id == home_team.id]
            away_players = [p for p in players_map.values() if p.team_id == away_team.id]
            
            boxscore_count = 0
            for player in home_players + away_players:
                is_star = player.name in star_players
                stats = generate_player_stats(player.name, is_star)
                
                boxscore = models.PlayerBoxscore(
                    game_id=game.id,
                    player_id=player.id,
                    **stats
                )
                db.add(boxscore)
                boxscore_count += 1
            
            print(f"  ✅ Maç {i+1}: {home_team.abbreviation} {home_score} - {away_score} {away_team.abbreviation} ({game_date}) - {boxscore_count} istatistik")
        
        db.commit()
        print(f"\n✅ {game_count} maç ve istatistikleri eklendi!")
        
        # 4. ML özellikleri hesapla (basit versiyon)
        print("\n🤖 ML özellikleri hesaplanıyor...")
        
        feature_count = 0
        for player in players_map.values():
            # Her oyuncu için son 5 maçın ortalamasını al
            recent_games = (
                db.query(models.PlayerBoxscore)
                .filter(models.PlayerBoxscore.player_id == player.id)
                .join(models.Game)
                .order_by(models.Game.date.desc())
                .limit(5)
                .all()
            )
            
            if recent_games:
                avg_pts = sum(g.points or 0 for g in recent_games) / len(recent_games)
                avg_reb = sum(g.rebounds or 0 for g in recent_games) / len(recent_games)
                avg_ast = sum(g.assists or 0 for g in recent_games) / len(recent_games)
                
                for boxscore in recent_games:
                    feature = models.PlayerFeatures(
                        player_id=player.id,
                        game_id=boxscore.game_id,
                        rolling_pts_5=round(avg_pts, 2),
                        rolling_reb_5=round(avg_reb, 2),
                        rolling_ast_5=round(avg_ast, 2),
                        matchup_difficulty_score=round(random.uniform(0.3, 0.8), 2),
                        rest_days=random.randint(0, 3),
                        target_above_avg=(boxscore.points or 0) > avg_pts
                    )
                    db.add(feature)
                    feature_count += 1
        
        db.commit()
        print(f"✅ {feature_count} ML özelliği eklendi!")
        
        # Özet
        print("\n" + "=" * 60)
        print("🎉 MOCK VERİ BAŞARIYLA OLUŞTURULDU!")
        print("=" * 60)
        print(f"📊 Takımlar: {len(TEAMS_DATA)}")
        print(f"👥 Oyuncular: {len(PLAYERS_DATA)}")
        print(f"🏆 Maçlar: {game_count}")
        print(f"📈 Oyuncu İstatistikleri: {len(home_players + away_players) * game_count}")
        print(f"🤖 ML Özellikleri: {feature_count}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Hata oluştu: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_mock_data()
