import os
import subprocess
import time
from pathlib import Path

import click


def make_job_script(name: str) -> str:
    """Make job script from given parameters

    Args:
        name (str): job name

    Returns:
        str: the content of job script file
    """
    job_script_content = (
        "#!/bin/zsh\n"
        f"#SBATCH -J {name}\n"
        "#SBATCH --nodes=1\n"
        "#SBATCH -o std.log\n"
        "#SBATCH -e err.log\n"
        "\n"
        "export MPI_PATH=/usr/local/calc/openmpi-gcc\n"
        "export PATH=${MPI_PATH}/bin:${PATH}\n"
        "export LD_LIBRARY_PATH=${MPI_PATH}/lib:${LD_LIBRARY_PATH}\n"
        "mpirun -np 16 /usr/local/calc/vasp/vasp544mpi"
    )

    return job_script_content


@click.command()
@click.option(
    "-p",
    "--partition",
    default="vega-a,vega-c",
    show_default=True,
    help="partition name",
)
def main(partition):
    """Usefull package to submit multiple phonon-tools jobs.

    search disp-0?? within current directory
    """
    root_dir_path = Path.cwd()
    for dir_path in root_dir_path.glob("disp-???"):
        job_script_path = dir_path / "job.sh"
        with job_script_path.open("w") as f:
            job_script_content = make_job_script(dir_path.stem)
            f.write(job_script_content)

        os.chdir(dir_path)
        subprocess.call(f"sbatch -p {partition} job.sh", shell=True)
        os.chdir(root_dir_path)

        # wait for safety
        time.sleep(0.1)


if __name__ == "__main__":
    main()
