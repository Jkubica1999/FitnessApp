from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from .workout import Exercise


# Base schema for GroupWorkout, shared by create and update schemas
class GroupWorkoutBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=2000)


# Schema for creating a new GroupWorkout
class GroupWorkoutCreate(GroupWorkoutBase):
    group_id: int
    exercises: List[Exercise] = Field(min_items=1)


# Schema for updating an existing GroupWorkout
class GroupWorkoutUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, min_length=1, max_length=2000)
    exercises: Optional[List[Exercise]] = None


# Output schema for returning GroupWorkout data to clients
class GroupWorkoutOut(BaseModel):
    id: int
    group_id: int
    created_by: int
    title: str
    description: str
    exercises: List[Exercise]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
