from pydantic import BaseModel, ConfigDict, Field


class StatsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teacher_id: int
    student_id: int
    group_id: int