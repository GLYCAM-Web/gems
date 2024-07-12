"""

Note/Fix: This and make_tleap_input replace external_bash/tleap.sh, however the simulation script delays tleap.sh's run until after slurm batching.
"""

import sys, subprocess

from gemsModules.complex.glycomimetics.tasks.make_tleap_input import make_tleap_input
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def run_tleap():
    subprocess.run(["tleap", "-f", "tleap.in"])


def run_ambpdb(prmtop_file, rst_file, output_pdb):
    with open(rst_file, "r") as rst_input:
        subprocess.run(
            ["ambpdb", "-p", prmtop_file],
            stdin=rst_input,
            text=True,
            stdout=open(output_pdb, "w"),
        )


def execute(analog_name, glycam_gaff_frcmod_exists):
    log.info(f"tleap sh analog name: {analog_name}")
    make_tleap_input(analog_name, glycam_gaff_frcmod_exists)
    run_tleap()
    run_ambpdb(
        f"{analog_name}_receptor_nowat_noion.prmtop",
        f"{analog_name}_receptor_nowat_noion.rst7",
        f"{analog_name}_receptor_nowat_noion.pdb",
    )
    run_ambpdb(
        f"{analog_name}_ligand_nowat_noion.prmtop",
        f"{analog_name}_ligand_nowat_noion.rst7",
        f"{analog_name}_ligand_nowat_noion.pdb",
    )
    run_ambpdb(
        f"{analog_name}_cocomplex_nowat_noion.prmtop",
        f"{analog_name}_cocomplex_nowat_noion.rst7",
        f"{analog_name}_cocomplex_nowat_noion.pdb",
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <analog_name> <glycam_gaff_frcmod_exists>")
    else:
        execute(sys.argv[1], sys.argv[2])
