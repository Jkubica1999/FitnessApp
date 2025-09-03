from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON 
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    athlete = "athlete"
    coach = "coach"
    parent = "parent"
    admin = "admin"
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.athlete, nullable=False) 
    created_at = Column(DateTime, default=datetime.now)

    workouts = relationship("Workout", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    mood_checkins = relationship("MoodCheckIn", back_populates="user")
    journal_entries = relationship("JournalEntry", back_populates="user")
    tests = relationship("Test", back_populates="user")
    summaries = relationship("Summary", back_populates="user")
    teams = relationship("Team", secondary="user_teams", back_populates="users")
    user_teams = relationship("UserTeams", back_populates="user")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    description = Column(String, nullable=False)
    exercises = Column(JSON, nullable=False) 

    user = relationship("User", back_populates="workouts")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    status = Column(Enum("pending", "in_progress", "completed", name="goal_status"), default="pending")

    user = relationship("User", back_populates="goals")

class MoodCheckIn(Base):
    __tablename__ = "mood_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="mood_checkins")

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    entry = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="journal_entries")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    results = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="tests")

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    period = Column(Enum("daily", "weekly", "monthly", name="summary_period"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    mood = Column(String, nullable=False)
    journal = Column(String, nullable=False)
    workout = Column(String, nullable=False)
    goals = Column(String, nullable=False)
    general = Column(String, nullable=False)

    user = relationship("User", back_populates="summaries")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    city = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    users = relationship("User", secondary="user_teams", back_populates="teams")
    groups = relationship("Group", back_populates="team")
    user_teams = relationship("UserTeams", back_populates="team", overlaps="users")
    user_teams = relationship("UserTeams", back_populates="team")

from sqlalchemy import UniqueConstraint

class Group(Base):
    __tablename__ = "groups"
    __table_args__ = (UniqueConstraint('team_id', 'name', name='_team_group_name_uc'),)

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    name = Column(String, nullable=False)

    team = relationship("Team", back_populates="groups")
    user_teams = relationship("UserTeams", back_populates="group")

class UserTeams(Base):
    __tablename__ = "user_teams"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    role = Column(Enum("member", "coach", "admin", name="team_role"), default="member")
    joined_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="user_teams")
    team = relationship("Team", back_populates="user_teams")
    group = relationship("Group", back_populates="user_teams")