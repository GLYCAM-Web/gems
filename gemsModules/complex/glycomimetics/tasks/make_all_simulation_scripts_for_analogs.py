# cd {simulation_dir}
# # for i in analog_* natural; do
# for i in analog_30 analog_37; do
#     # We are replicating this elsewhere. See run_master_submit.py
#     # {glycomimetic_scripts_dir}/make_simulation_scripts.sh ${{i}}
#     sbatch slurm_submit_${{i}}.sh
#     sleep 1
# done

# replicating just the make_sim scripts call in python given we can import it as a task

from gemsModules.complex.glycomimetics.tasks.make_simulation_scripts import (
    execute as make_simulation_scripts,
)


# TODO/NOTE: This is so empty because we're relying on bash environmental-fu. Fix this where sensible.
def execute():
    # for i in analog_* natural; do
    # as a glob in python:
    # glob.glob(f"{simulation_dir}/analog_*")
    for i in ["analog_30", "analog_37"]:
        make_simulation_scripts(i)
