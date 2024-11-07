from pathlib import Path

from pydantic import BaseModel, Field


class ArrayJobParameters(BaseModel):
    job_name: str
    partition: str
    commands: list[str]
    gpu_resources: str = Field(default="")
    parallel_count: int = Field(default=1)
    preamble: str = Field(default="")
    output_log_path: Path = Field(default=Path(r"./output.%j.%a.log"))
    output_error_path: Path = Field(default=Path(r"./error.%j.%a.log"))
    script_directory: Path = Field(default=Path("."))

    def model_post_init(self, __context):
        # Resolving paths
        self.output_error_path = self.output_error_path.resolve()
        self.output_log_path = self.output_log_path.resolve()
        self.script_directory = self.script_directory.resolve()


class _ArrayJobParametersInTemplate(BaseModel):
    job_name: str
    output_log_path: Path
    output_error_path: Path
    partition: str
    gpu_resources: str
    line_count: int
    parallel_count: int
    commands_file: Path
    preamble: str = Field(default="")
