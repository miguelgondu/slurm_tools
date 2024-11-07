from tempfile import TemporaryDirectory

from slurm_tools.jobs.array import parallelize_commands_in_array_job
from slurm_tools.parameters import ArrayJobParameters


def test_array_job_creation_from_commands():
    commands = [
        "python --version",
        "python -c 'print(1)'",
        "python -c 'print(2)'",
    ]

    parameters = ArrayJobParameters(
        job_name="test_array_job",
        partition="test",
        commands=commands,
        script_directory=TemporaryDirectory().name,
    )

    parallelize_commands_in_array_job(commands, parameters)

    job_directory = parameters.script_directory / parameters.job_name

    assert (job_directory / "commands.txt").exists()
    assert (job_directory / "commands.txt").read_text() == "\n".join(commands)
    assert (job_directory / "array_job.sh").exists()
    assert (job_directory / "readme.md").exists()
    assert (job_directory / ".gitignore").exists()


if __name__ == "__main__":
    test_array_job_creation_from_commands()
