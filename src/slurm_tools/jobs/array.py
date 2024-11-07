"""
Implements a simple interface to array jobs in SLURM.
"""

from pathlib import Path

from slurm_tools.parameters import ArrayJobParameters, _ArrayJobParametersInTemplate
from slurm_tools.utils.reading_templates import read_template


def _parse_array_job_parameters_for_template(
    parameters: ArrayJobParameters,
) -> _ArrayJobParametersInTemplate:
    """
    Parse the array job parameters for the template.

    Args:
        parameters (ArrayJobParameters): The parameters for the array job.

    Returns:
        _ArrayJobParametersInTemplate: The parameters for the template.
    """
    return _ArrayJobParametersInTemplate(
        job_name=parameters.job_name,
        output_log_path=parameters.output_log_path,
        output_error_path=parameters.output_error_path,
        partition=parameters.partition,
        gpu_resources=parameters.gpu_resources,
        line_count=len(parameters.commands),
        parallel_count=parameters.parallel_count,
        commands_file=parameters.script_directory / "commands.txt",
    )


def _get_job_directory(parameters: ArrayJobParameters) -> Path:
    """
    Get the job directory.

    Args:
        parameters (ArrayJobParameters): The parameters for the array job.

    Returns:
        job_directory (Path): The job directory.
    """
    return parameters.script_directory / parameters.job_name.replace(" ", "_")


def _create_job_directory(parameters: ArrayJobParameters):
    """
    Create the job directory.

    Args:
        parameters (ArrayJobParameters): The parameters for the array job.
    """
    _get_job_directory(parameters).mkdir(parents=True, exist_ok=True)


def _write_commands(commands: list[str], parameters: ArrayJobParameters):
    """
    Write the commands to a file.

    Args:
        commands (list[str]): The commands to write.
        parameters (ArrayJobParameters): The parameters for the array job.
    """
    _create_job_directory(parameters)
    with open(_get_job_directory(parameters) / "commands.txt", "w") as commands_file:
        for command in commands:
            commands_file.write(f"{command}\n")


def parallelize_commands_in_array_job(
    commands: list[str],
    array_parameters: ArrayJobParameters,
) -> None:
    """
    Write a SLURM array job script from a list of commands.

    Args:
        commands (list[str]): The commands to run in the array job.
        parameters (ArrayJobParameters): The parameters for the array job.
    """
    template = read_template("array_template")

    _create_job_directory(array_parameters)

    _write_commands(commands, array_parameters)

    with open(
        _get_job_directory(array_parameters) / ".gitignore", "w"
    ) as gitignore_file:
        gitignore_file.write("*\n")

    template_parameters = _parse_array_job_parameters_for_template(array_parameters)

    with open(
        _get_job_directory(array_parameters) / "array_job.sh", "w"
    ) as script_file:
        script_file.write(template.render(**template_parameters.model_dump()))
