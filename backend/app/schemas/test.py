# Test data validation and serialization schemas
from datetime import datetime
from typing import List, Optional

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
    kilograms = "kg"
    pounds = "lb"

class DistanceEnum(str, Enum):
    meters = "m"
    kilometers = "km"
    miles = "mi"
    yards = "yd"

class TimeEnum(str, Enum):
    seconds = "s"
    minutes = "min"
    hours = "h"

class HeightEnum(str, Enum):
    centymeters = "cm"
    inches = "in"

class LengthEnum(str, Enum):
    centymeters = "cm"
    meters = "m"
    inches = "in"

METRIC_UNITS = {
    MetricTypeEnum.weight: WeightEnum,
    MetricTypeEnum.distance: DistanceEnum,
    MetricTypeEnum.time: TimeEnum,
    MetricTypeEnum.height: HeightEnum,
    MetricTypeEnum.length: LengthEnum,
    # reps, heart_rate, rpe are unitless
}

# Helper function to validate unit based on metric type
def validate_unit_for_type(metric_type: MetricTypeEnum, unit: Optional[str]) -> Optional[str]:
    unit_enum = METRIC_UNITS.get(metric_type)

    if unit_enum:
        allowed = {e.value for e in unit_enum}
        if unit not in allowed:
            raise ValueError(f"Invalid unit '{unit}' for metric type '{metric_type}'. Allowed: {allowed}")
    else:
        if unit is not None:
            raise ValueError(f"Metric type '{metric_type}' should not have a unit")

    return unit

# Schema for individual metric details
class MetricEntry(BaseModel):
    type: MetricTypeEnum
    unit: Optional[str] = None  # Unit depends on type

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v, values):
        metric_type = values.get("type")
        if metric_type is None:
            return v
        return validate_unit_for_type(metric_type, v)

# Schema for parameters of a test
class TestParameter(BaseModel):
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
        if metric_type is None:
            return v
        return validate_unit_for_type(metric_type, v)
    
#base schema for Test, shared by create and update schemas
class TestBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    instructions: Optional[str] = Field(default=None, max_length=2000)

# Schema for creating a new Test
class TestCreate(TestBase):
    parameters: List[TestParameter]

    @field_validator("parameters")
    @classmethod
    def parameters_must_have_at_least_one(cls, v):
        if not v or len(v) < 1:
            raise ValueError("At least one parameter is required")
        return v
    
# Schema for updating an existing Test
class TestUpdate(TestBase):
    parameters: Optional[List[TestParameter]] = None

    @field_validator("parameters")
    @classmethod
    def parameters_must_have_at_least_one_if_provided(cls, v):
        if v is not None and len(v) < 1:
            raise ValueError("At least one parameter is required if parameters are provided")
        return v

# Schema for recording results of a taken Test
class TestResult(BaseModel):
    taken_at: datetime = Field(default_factory=datetime.now)
    results: List[MetricResult]

    @field_validator("results")
    @classmethod
    def results_must_have_at_least_one(cls, v):
        if not v or len(v) < 1:
            raise ValueError("At least one result is required")
        return v
    
# Full schema for reading a Test with all details
class TestOut(TestBase):
    id: int
    user_id: int
    group_test_id: Optional[int] = None
    parameters: List[TestParameter]
    created_at: datetime
    taken_at: Optional[datetime] = None
    results: Optional[List[MetricResult]] = None

    model_config = ConfigDict(from_attributes=True)