import os
import subprocess
import sys

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

# TODO: unify with make_simulation_scripts.py
GLYCOMIMETICS_SCRIPTS_DIR = (
    os.getenv("GEMSHOME")
    + "/gemsModules/complex/glycomimetics/docs/tasks_reference/external_scripts_bash"
)


def write_slurm_script(job_workdir_abs, glycomimetic_scripts_dir):
    # Note, job_workdir is equivalent to job_workdir_absolute in the original bash script
    glycomimetic_dir = os.path.join(job_workdir_abs, "glycomimetics")
    simulation_dir = os.path.join(job_workdir_abs, "simulation")
    glycomimetic_input_file = os.path.join(glycomimetic_dir, "sample_input_file.txt")
    glycomimetic_output_dir = "output"
    num_cpus_glycomimetics = 4

    script_content = f"""#!/bin/bash
#SBATCH -D {job_workdir_abs}
#SBATCH -J glycomimetics
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node={num_cpus_glycomimetics}

source /etc/profile.d/modules.sh

cd {glycomimetic_dir}
# TODO: Does nothing, copied from reference, input file seems unused - possibly expected reference for GEMS, but input file format never used?
# {glycomimetic_dir}/main.exe -f {glycomimetic_input_file}
# exit 1

# Now make simulation directories, one for each analog
cd {job_workdir_abs}
glycomimetic_output_dir_with_slash="{glycomimetic_dir}/{glycomimetic_output_dir}"


# TODO: Replace with PM service, for now run_master_submit.py performs this function before sbatching. 
# {glycomimetic_scripts_dir}/makedir.sh ${{glycomimetic_output_dir_with_slash}} {simulation_dir}

# For GEMS testing, only do the 1st glycomimetic step. Bail here. (TODO: use gems testing workflow var)
exit 1

cd {simulation_dir}
# for i in analog_* natural; do
for i in analog_30 analog_37; do
    {glycomimetic_scripts_dir}/make_simulation_scripts.sh ${{i}}
    sbatch slurm_submit_${{i}}.sh
    sleep 1
done
echo 'Slurm glycomimetic script reaches end'
"""
    slurm_script_path = os.path.join(job_workdir_abs, "slurm_submit_glycomimetics.sh")
    with open(slurm_script_path, "w") as f:
        f.write(script_content)
        log.debug(f"Wrote Slurm script to {slurm_script_path}")

    return slurm_script_path


def execute(job_workdir):
    slurm_script_path = write_slurm_script(job_workdir, GLYCOMIMETICS_SCRIPTS_DIR)

    return slurm_script_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <job_workdir>")
    else:
        # convenience for testing
        os.makedirs(sys.argv[1], exist_ok=True)
        execute(sys.argv[1])
