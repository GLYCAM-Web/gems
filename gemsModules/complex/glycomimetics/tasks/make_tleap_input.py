import subprocess
import sys


# TODO: use project dir
def execute(analog_name, glycam_gaff_frcmod_exists, project_dir=None):
    receptor_pdb = f"{analog_name}_receptor.pdb"
    glycam_gaff_off = f"{analog_name}_glycam_gaff.off"
    glycam_gaff_frcmod = f"{analog_name}_glycam_gaff.frcmod"

    with open("tleap.in", "w") as file:
        file.write(
            f"""source leaprc.GLYCAM_06j-1
source leaprc.protein.ff14SB
source leaprc.gaff
loadamberparams frcmod.ions234lm_1264_tip3p
loadamberparams corona.frcmod
"""
        )
        if glycam_gaff_frcmod_exists == "true":
            file.write(f"loadamberparams {glycam_gaff_frcmod}\n")
        file.write(
            f"""receptor = loadpdb {receptor_pdb}
saveamberparm receptor receptor_nowat_noion.prmtop receptor_nowat_noion.rst7
loadOff {glycam_gaff_off}
ligand = sequence{{corona}}
saveamberparm ligand ligand_nowat_noion.prmtop ligand_nowat_noion.rst7
cocomplex = combine {{receptor ligand}}
saveamberparm cocomplex cocomplex_nowat_noion.prmtop cocomplex_nowat_noion.rst7
addIons receptor Na+ 0
addIons receptor Cl- 0
solvateoct receptor TIP3PBOX 10.0 iso
saveamberparm receptor receptor.prmtop receptor.rst7
addIons ligand Na+ 0
addIons ligand Cl- 0
solvateoct ligand TIP3PBOX 10.0 iso
saveamberparm ligand ligand.prmtop ligand.rst7
addIons cocomplex Na+ 0
addIons cocomplex Cl- 0
solvateoct cocomplex TIP3PBOX 10.0 iso
saveamberparm cocomplex cocomplex.prmtop cocomplex.rst7
quit
"""
        )
