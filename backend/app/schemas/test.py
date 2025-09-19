# Test data validation and serialization schemas
from datetime import datetime
from typing import List, Optional, Annotated

from pydantic import BaseModel, Field, ConfigDict, field_validator
from enum import Enum

# Enum for metrics types
class MetricTypeEnum(str, Enum):
    weight = "weight"
    reps = "reps"
    time = "time"
    distance = "distance"
    heart_rate = "heart_rate"
    rpe = "rpe"  # Rate of Perceived Exertion
    height = "height"
    length = "length"

# Enum for units of measurement for each metric type
class WeightEnum(str, Enum):
    kg = "kg"
    lbs = "lbs"

class DistanceEnum(str, Enum):
    meters = "meters"
    km = "km"
    miles = "miles"
    yards = "yards"

class TimeEnum(str, Enum):
    seconds = "sec"
    minutes = "min"
    hours = "hrs"

class HeightEnum(str, Enum):
    cm = "cm"
    inches = "in"

class LengthEnum(str, Enum):
    cm = "cm"
    meters = "meters"
    inches = "in"

# Schema for individual metric details
class MetricEntry(BaseModel):
    type: MetricTypeEnum
    unit: Optional[str] = None  # Unit depends on type

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v, values):
        metric_type = values.get("type")
        if metric_type == MetricTypeEnum.weight:
            if v not in {e.value for e in WeightEnum}:
                raise ValueError(f"Invalid unit for weight: {v}")
        elif metric_type == MetricTypeEnum.distance:
            if v not in {e.value for e in DistanceEnum}:
                raise ValueError(f"Invalid unit for distance: {v}")
        elif metric_type == MetricTypeEnum.time:
            if v not in {e.value for e in TimeEnum}:
                raise ValueError(f"Invalid unit for time: {v}")
        elif metric_type == MetricTypeEnum.height:
            if v not in {e.value for e in HeightEnum}:
                raise ValueError(f"Invalid unit for height: {v}")
        elif metric_type == MetricTypeEnum.length:
            if v not in {e.value for e in LengthEnum}:
                raise ValueError(f"Invalid unit for length: {v}")
        elif metric_type in {MetricTypeEnum.reps, MetricTypeEnum.heart_rate, MetricTypeEnum.rpe}:
            if v is not None:
                raise ValueError(f"No unit should be provided for type: {metric_type}")
        return v

# Base schema for parameters
class TestParameterBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    metrics: List[MetricEntry]

    @field_validator("metrics")
    @classmethod
    def metrics_must_have_at_least_one(cls, v):
        if not v or len(v) < 1:
            raise ValueError("At least one metric is required")
        return v
    
# Schema for results of a test parameter
class MetricResult(BaseModel):
    type: MetricTypeEnum
    value: float = Field(..., ge=0)
    unit: Optional[str] = None  # Unit depends on type

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v, values):
        metric_type = values.get("type")
        if metric_type == MetricTypeEnum.weight:
            if v not in {e.value for e in WeightEnum}:
                raise ValueError(f"Invalid unit for weight: {v}")
        elif metric_type == MetricTypeEnum.distance:
            if v not in {e.value for e in DistanceEnum}:
                raise ValueError(f"Invalid unit for distance: {v}")
        elif metric_type == MetricTypeEnum.time:
            if v not in {e.value for e in TimeEnum}:
                raise ValueError(f"Invalid unit for time: {v}")
        elif metric_type == MetricTypeEnum.height:
            if v not in {e.value for e in HeightEnum}:
                raise ValueError(f"Invalid unit for height: {v}")
        elif metric_type == MetricTypeEnum.length:
            if v not in {e.value for e in LengthEnum}:
                raise ValueError(f"Invalid unit for length: {v}")
        elif metric_type in {MetricTypeEnum.reps, MetricTypeEnum.heart_rate, MetricTypeEnum.rpe}:
            if v is not None:
                raise ValueError(f"No unit should be provided for type: {metric_type}")
        return v
         
