import os
import sys
import subprocess

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

G16_ROOT = "/programs/gaussian/16"


def execute(dirname, num_cpus_emin=7, num_cpus_gbsa=7, num_mem_gaussian="1024MB"):
    root_dir = "/home/yao"

    # Get directory name from command line arguments
    dirname = sys.argv[1]

    # Set environment variables
    os.environ["dirname"] = dirname
    os.environ["autogen_input_path"] = (
        f"{root_dir}/glycomimetics/autogen_md_input_files"
    )
    os.environ["interface_glycam_gaff_path"] = (
        f"{root_dir}/glycomimetics/glycam_gaff_interfacing"
    )
    os.environ["glycomimetic_program_dir"] = f"{root_dir}/glycomimetics"
    os.environ["glycomimetics_scripts_dir"] = (
        os.getenv("GEMSHOME")
        + "/gemsModules/complex/glycomimetics/docs/tasks_reference/external_scripts_bash"
    )
    os.environ["num_cpus_emin"] = str(num_cpus_emin)
    os.environ["num_cpus_gbsa"] = str(num_cpus_gbsa)
    os.environ["num_mem_gaussian"] = num_mem_gaussian
    os.environ["g16root"] = G16_ROOT

    # Determine analog_name based on dirname
    if dirname == "natural_ligand":
        analog_name = "natural"
    else:
        analog_name = dirname.replace("analog_", "")

    log.debug(f"Processing {analog_name}")

    os.environ["ligand_pdb"] = f"{analog_name}_ligand.pdb"

    # List of scripts to run - using local dir to the GEMS task for now.
    gen_scripts_dir = f"{os.path.dirname(__file__)}/simulation_scripts_src"
    scripts = [
        "make_1_slurm.sh",
        "make_2_md.sh",
        "make_3_emin.sh",
        "make_4_gbsa.sh",
    ]

    # Execute each script
    for script in scripts:
        script = f"{gen_scripts_dir}/{script}"
        result = subprocess.run([script], shell=True)
        if result.returncode != 0:
            log.warning(f"Error executing {script}")
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <dirname>")
    else:
        execute(sys.argv[1])
