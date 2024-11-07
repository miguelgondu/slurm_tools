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
    )

    parallelize_commands_in_array_job(commands, parameters)


if __name__ == "__main__":
    test_array_job_creation_from_commands()
