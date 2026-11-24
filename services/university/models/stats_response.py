from pydantic import BaseModel, ConfigDict, Field


class StatsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    count: int
    min: int
    max: int
    avg: float