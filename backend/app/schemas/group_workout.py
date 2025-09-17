from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from .workout import Exercise


class GroupWorkoutBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=2000)


class GroupWorkoutCreate(GroupWorkoutBase):
    group_id: int
    exercises: List[Exercise] = Field(min_items=1)


class GroupWorkoutUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, min_length=1, max_length=2000)
    exercises: Optional[List[Exercise]] = None


class GroupWorkoutOut(BaseModel):
    id: int
    group_id: int
    created_by: int
    title: str
    description: str
    exercises: List[Exercise]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
