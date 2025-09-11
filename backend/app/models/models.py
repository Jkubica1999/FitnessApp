from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Boolean, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    athlete = "athlete"
    coach = "coach"

class PeriodEnum(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    workouts = relationship("Workout", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    mood_checkins = relationship("MoodCheckIn", back_populates="user")
    journal_entries = relationship("JournalEntry", back_populates="user")
    tests = relationship("Test", back_populates="user")
    summaries = relationship("Summary", back_populates="user")
    user_teams = relationship("UserTeams", back_populates="user")
    teams = association_proxy("user_teams", "team")
    groups = association_proxy("user_teams", "group")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    group_workout_id = Column(Integer, ForeignKey("group_workouts.id", ondelete="SET NULL"), index=True, nullable=True)
    title = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    description = Column(String, nullable=False)
    exercises = Column(JSON, nullable=False) 
    results = Column(JSON, nullable=True)
    update_log = Column(JSON, nullable=True)   # history of changes, deload weeks, notes
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="workouts")

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    group_test_id = Column(Integer, ForeignKey("group_tests.id", ondelete="SET NULL"), index=True, nullable=True)
    title = Column(String, nullable=False)
    instructions = Column(String)
    parameters = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    taken_at = Column(DateTime)
    results = Column(JSON)

    user = relationship("User", back_populates="tests")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="goals")

class MoodCheckIn(Base):
    __tablename__ = "mood_checkins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    mood = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="mood_checkins")

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    entry = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="journal_entries")

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    period = Column(Enum(PeriodEnum), default=PeriodEnum.daily, nullable=False)
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
    name = Column(String, unique=True, index=True, nullable=False)
    city = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    groups = relationship("Group", back_populates="team")
    user_teams = relationship("UserTeams", back_populates="team")
    users = association_proxy("user_teams", "user")

class Group(Base):
    __tablename__ = "groups"
    __table_args__ = (
        UniqueConstraint('team_id', 'name', name='_team_group_name_uc'),
        UniqueConstraint("id", "team_id", name="uq_group_id_team"),
    )

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), index=True, nullable=False)
    name = Column(String, nullable=False)

    team = relationship("Team", back_populates="groups")
    user_teams = relationship("UserTeams", back_populates="group")
    users = association_proxy("user_teams", "user")

    group_workouts = relationship("GroupWorkout", back_populates="group")
    group_tests = relationship("GroupTest", back_populates="group")

class UserTeams(Base):
    __tablename__ = "user_teams"
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', 'role', name='uq_user_group_role'),
        ForeignKeyConstraint(['group_id', 'team_id'], ['groups.id', 'groups.team_id'], name='fk_group_team'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), index=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), index=True, nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.athlete, nullable=False)
    is_team_admin = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="user_teams")
    team = relationship("Team", back_populates="user_teams")
    group = relationship("Group", back_populates="user_teams")

class GroupWorkout(Base):
    __tablename__ = "group_workouts"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime)
    description = Column(String, nullable=False)
    exercises = Column(JSON, nullable=False)  
    created_at = Column(DateTime, default=datetime.now)

    group = relationship("Group", back_populates="group_workouts")
    coach = relationship("User")

class GroupTest(Base):
    __tablename__ = "group_tests"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String, nullable=False)
    instructions = Column(String)
    parameters = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    group = relationship("Group", back_populates="group_tests")
    coach = relationship("User")