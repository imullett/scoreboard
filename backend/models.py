from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import registry
from dataclasses import asdict

reg = registry()

@reg.mapped_as_dataclass
class GameData:
    __tablename__ = 'game'

    gameId: int = Column(Integer, nullable=True)
    teamId: int = Column(Integer, primary_key=True, nullable=False)
    weekNumber: int = Column(Integer, primary_key=True, nullable=False)
    totalPoints: float = Column(Float, nullable=True)
    projectedPoints: float = Column(Float, nullable=True)
    # qb: str = Column(String, nullable=True)
    # qbPoints: float = Column(Float, nullable=True)
    # wr1: str = Column(String, nullable=True)
    # wr1Points: float = Column(Float, nullable=True)
    # wr2: str = Column(String, nullable=True)
    # wr2Points: float = Column(Float, nullable=True)
    # rb1: str = Column(String, nullable=True)
    # rb1Points: float = Column(Float, nullable=True)
    # rb2: str = Column(String, nullable=True)
    # rb2Points: float = Column(Float, nullable=True)
    # te: str = Column(String, nullable=True)
    # tePoints: float = Column(Float, nullable=True)
    # flex: str = Column(String, nullable=True)
    # flexPoints: float = Column(Float, nullable=True)
    # kicker: str = Column(String, nullable=True)
    # kickerPoints: float = Column(Float, nullable=True)
    # defense: str = Column(String, nullable=True)
    # defensePoints: float = Column(Float, nullable=True)
    # bn1: str = Column(String, nullable=True)
    # bn1Points: float = Column(Float, nullable=True)
    # bn2: str = Column(String, nullable=True)
    # bn2Points: float = Column(Float, nullable=True)
    # bn3: str = Column(String, nullable=True)
    # bn3Points: float = Column(Float, nullable=True)
    # bn4: str = Column(String, nullable=True)
    # bn4Points: float = Column(Float, nullable=True)
    __table_args__ = (
        UniqueConstraint('teamId', 'weekNumber', name='UK_game_team_week'),
    )
    def to_dict(self):
        return asdict(self)

@reg.mapped_as_dataclass
class TeamData:
    __tablename__ = 'team'

    teamId: int = Column(Integer, primary_key=True, autoincrement=True)
    teamName: str = Column(String(255), nullable=False)
    yahooId: str = Column(String(255), nullable=False)
    profilePicture: str = Column(String(1000), nullable=False)
    manager: str = Column(String(255), nullable=False)

    def to_dict(self):
        return asdict(self)

@reg.mapped_as_dataclass
class MatchupData:
    __tablename__ = 'matchup'

    matchupId: int = Column(Integer, primary_key=True, autoincrement=True)
    weekNumber: int = Column(Integer, nullable=False)
    team1Id: int = Column(Integer, nullable=False)
    team2Id: int = Column(Integer, nullable=False)
    team3Id: int = Column(Integer, nullable=False)

    def to_dict(self):
        return asdict(self)


@reg.mapped_as_dataclass
class CurrentWeek:
    __tablename__ = 'currentweek'

    id: int = Column(Integer, primary_key=True)
    number: int = Column(Integer, nullable=False)