from pathlib import Path

from pydantic import BaseModel, Field


class ArrayJobParameters(BaseModel):
    job_name: str
    partition: str
    commands: list[str]
    gpu_resources: str = Field(default="")
    parallel_count: int = Field(default=1)
    output_log_path: Path = Field(default=Path(r"./output.%j.%a.log"))
    output_error_path: Path = Field(default=Path(r"./error.%j.%a.log"))
    script_directory: Path = Field(default=Path("."))


class _ArrayJobParametersInTemplate(BaseModel):
    job_name: str
    output_log_path: Path
    output_error_path: Path
    partition: str
    gpu_resources: str
    line_count: int
    parallel_count: int
    commands_file: Path
