from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, registry, Session
from abc import ABC, abstractmethod

reg = registry()

@reg.mapped_as_dataclass
class GameData:
    __tablename__ = 'game'

    gameId: int = Column(Integer, primary_key=True, autoincrement=True)
    teamId: int = Column(Integer, nullable=False)
    weekNumber: int = Column(Integer, nullable=False)
    totalPoints: float = Column(Float, nullable=True)
    projectedPoints: float = Column(Float, nullable=True)
    qb: str = Column(String, nullable=True)
    qbPoints: float = Column(Float, nullable=True)
    wr1: str = Column(String, nullable=True)
    wr1Points: float = Column(Float, nullable=True)
    wr2: str = Column(String, nullable=True)
    wr2Points: float = Column(Float, nullable=True)
    rb1: str = Column(String, nullable=True)
    rb1Points: float = Column(Float, nullable=True)
    rb2: str = Column(String, nullable=True)
    rb2Points: float = Column(Float, nullable=True)
    te: str = Column(String, nullable=True)
    tePoints: float = Column(Float, nullable=True)
    flex: str = Column(String, nullable=True)
    flexPoints: float = Column(Float, nullable=True)
    kicker: str = Column(String, nullable=True)
    kickerPoints: float = Column(Float, nullable=True)
    defense: str = Column(String, nullable=True)
    defensePoints: float = Column(Float, nullable=True)
    bn1: str = Column(String, nullable=True)
    bn1Points: float = Column(Float, nullable=True)
    bn2: str = Column(String, nullable=True)
    bn2Points: float = Column(Float, nullable=True)
    bn3: str = Column(String, nullable=True)
    bn3Points: float = Column(Float, nullable=True)
    bn4: str = Column(String, nullable=True)
    bn4Points: float = Column(Float, nullable=True)

@reg.mapped_as_dataclass
class TeamData:
    __tablename__ = 'team'

    teamId: int = Column(Integer, primary_key=True, autoincrement=True)
    teamName: str = Column(String(255), nullable=False)
    yahooId: str = Column(String(255), nullable=False)
    manager: str = Column(String(255), nullable=False)