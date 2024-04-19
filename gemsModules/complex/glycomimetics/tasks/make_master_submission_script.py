import os
import subprocess
import sys


def write_slurm_script(job_workdir, glycomimetic_scripts_dir):
    job_workdir_absolute = os.path.abspath(job_workdir)
    glycomimetic_dir = os.path.join(job_workdir_absolute, "glycomimetics")
    simulation_dir = os.path.join(job_workdir_absolute, "simulation")
    glycomimetic_input_file = os.path.join(glycomimetic_dir, "sample_input_file.txt")
    glycomimetic_output_dir = "output"
    num_cpus_glycomimetics = 4

    script_content = f"""#!/bin/bash
#SBATCH -D {job_workdir_absolute}
#SBATCH -J glycomimetics
#SBATCH --get-user-env
#SBATCH --nodes=1
#SBATCH --tasks-per-node={num_cpus_glycomimetics}

source /etc/profile.d/modules.sh

cd {glycomimetic_dir}
# {glycomimetic_dir}/main.exe -f {glycomimetic_input_file}
# exit 1

# Now make simulation directories, one for each analog
cd {job_workdir_absolute}
glycomimetic_output_dir_with_slash="{glycomimetic_dir}/{glycomimetic_output_dir}"

{glycomimetic_scripts_dir}/makedir.sh ${glycomimetic_output_dir_with_slash} {simulation_dir}

# For GEMS testing, only do the 1st glycomimetic step. Bail here. (TODO: use gems testing workflow var)
exit 1

cd {simulation_dir}
# for i in analog_* natural; do
for i in analog_30 analog_37; do
    {glycomimetic_scripts_dir}/make_simulation_scripts.sh ${i}
    sbatch slurm_submit_${i}.sh
    sleep 1
done
echo 'Slurm glycomimetic script reaches end'
"""
    slurm_script_path = os.path.join(
        job_workdir_absolute, "slurm_submit_glycomimetics.sh"
    )
    with open(slurm_script_path, "w") as f:
        f.write(script_content)
    return slurm_script_path


def execute(job_workdir):
    glycomimetic_scripts_dir = "/home/yao/glycomimetic_simulations/scripts"
    slurm_script_path = write_slurm_script(job_workdir, glycomimetic_scripts_dir)

    # TODO: run the script
    # Submitting the Slurm job
    # subprocess.run(["sbatch", slurm_script_path])


if __name__ == "__main__":
    execute(sys.argv[1])
