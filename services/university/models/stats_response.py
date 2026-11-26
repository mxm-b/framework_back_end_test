from pydantic import BaseModel, ConfigDict, model_validator, Field
from typing import Self
from .base_grade import MIN_GRADE, MAX_GRADE


class StatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int
    min: int | None = Field(ge=MIN_GRADE, le=MAX_GRADE)
    max: int | None = Field(ge=MIN_GRADE, le=MAX_GRADE)
    avg: float | None = Field(ge=MIN_GRADE, le=MAX_GRADE)

    @model_validator(mode="after")
    def check_values(self) -> Self:
        if self.count < 0:
            raise ValueError("count must be >= 0")
        if self.count == 0:
            if self.min is not None or self.max is not None or self.avg is not None:
                raise ValueError("min, max and avg must be 'None'")
            return self
        if self.min is None or self.max is None or self.avg is None:
            raise ValueError("min, max and avg must have values")
        if self.min > self.max:
            raise ValueError("min must be <= max")
        if self.avg < self.min or self.avg > self.max:
            raise ValueError("avg must be >= min and <= max")
        return self