# Workout data validation and serialization schemas
from datetime import datetime
from typing import List, Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict


# SetEntry schema for individual set details in an exercise
class SetEntry(BaseModel):
    set: Annotated[int, Field(ge=1, description="1-based set index")]
    reps: Annotated[int, Field(ge=0, description="Target or performed reps")]
    weight: Optional[Annotated[float, Field(ge=0, description="Weight (kg)")]] = None
    rest_sec: Optional[Annotated[int, Field(ge=0, description="Rest time after this set, in seconds")]] = None
    note: Optional[str] = None


# Exercise schema containing a name and a list of sets
class Exercise(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    sets: List[SetEntry] = Field(min_items=1)


# ExerciseResult schema for storing results of performed exercises
class ExerciseResult(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    sets: List[SetEntry] = Field(min_items=1)


# UpdateLogEntry schema for tracking changes to a workout
class UpdateLogEntry(BaseModel):
    at: datetime = Field(default_factory=datetime.now)
    change: str = Field(min_length=1, max_length=500)
    meta: Optional[dict] = Field(default=None, description="Optional structured details of the change")


# Base schema for Workout, shared by create and update schemas
class WorkoutBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=2000)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    group_workout_id: Optional[int] = Field(
        default=None, description="If adopted from a GroupWorkout, reference it here"
    )


# Schema for creating a new Workout
class WorkoutCreate(WorkoutBase):
    exercises: List[Exercise] = Field(min_items=1)
    results: Optional[List[ExerciseResult]] = None
    update_log: Optional[List[UpdateLogEntry]] = None


# Schema for updating an existing Workout
class WorkoutUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, min_length=1, max_length=2000)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    group_workout_id: Optional[int] = None
    exercises: Optional[List[Exercise]] = None
    results: Optional[List[ExerciseResult]] = None
    update_log: Optional[List[UpdateLogEntry]] = None


# Output schema for returning Workout data to clients
class WorkoutOut(BaseModel):
    id: int
    user_id: int
    group_workout_id: Optional[int]
    title: str
    description: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    exercises: List[Exercise]
    results: Optional[List[ExerciseResult]] = None
    update_log: Optional[List[UpdateLogEntry]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
