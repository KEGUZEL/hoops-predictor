from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    api_team_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)
    conference = Column(String, nullable=True)
    division = Column(String, nullable=True)

    players = relationship("Player", back_populates="team")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    api_player_id = Column(String, unique=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    name = Column(String, nullable=False)
    position = Column(String, nullable=True)

    team = relationship("Team", back_populates="players")
    boxscores = relationship("PlayerBoxscore", back_populates="player")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    api_game_id = Column(String, unique=True, index=True)
    season = Column(Integer, index=True)
    date = Column(Date, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)


class PlayerBoxscore(Base):
    __tablename__ = "player_boxscores"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player_id = Column(Integer, ForeignKey("players.id"))

    minutes = Column(Float, nullable=True)
    points = Column(Integer, nullable=True)
    rebounds = Column(Integer, nullable=True)
    assists = Column(Integer, nullable=True)
    fgm = Column(Integer, nullable=True)
    fga = Column(Integer, nullable=True)
    ftm = Column(Integer, nullable=True)
    fta = Column(Integer, nullable=True)
    tpm = Column(Integer, nullable=True)
    tpa = Column(Integer, nullable=True)
    turnovers = Column(Integer, nullable=True)
    plus_minus = Column(Integer, nullable=True)

    player = relationship("Player", back_populates="boxscores")


class PlayerFeatures(Base):
    __tablename__ = "player_features"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    game_id = Column(Integer, ForeignKey("games.id"), index=True)

    rolling_pts_5 = Column(Float, nullable=True)
    rolling_reb_5 = Column(Float, nullable=True)
    rolling_ast_5 = Column(Float, nullable=True)
    matchup_difficulty_score = Column(Float, nullable=True)
    rest_days = Column(Integer, nullable=True)

    target_above_avg = Column(Boolean, nullable=True)

