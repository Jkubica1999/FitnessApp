# GroupTest schema for grouping tests
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

from .test import TestParameter

# GRoup Test base schema, shared by create and update schemas
class GroupTestBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    instructions: str = Field(min_length=1, max_length=2000)

# Schema for creating a new GroupTest
class GroupTestCreate(GroupTestBase):    
    group_id: int
    parameters: List[TestParameter]

    @field_validator("parameters")
    @classmethod
    def validate_parameters(cls, value):
        if not value or len(value) < 1:
            raise ValueError("At least one parameter is required.")
        return value

# Schema for updating an existing GroupTest
class GroupTestUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    instructions: Optional[str] = Field(default=None, min_length=1, max_length=2000)
    parameters: Optional[List[TestParameter]] = None

# Output schema for returning GroupTest data to clients
class GroupTestOut(BaseModel):
    id: int
    group_id: int
    created_by: int
    title: str
    instructions: str
    parameters: List[TestParameter]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)