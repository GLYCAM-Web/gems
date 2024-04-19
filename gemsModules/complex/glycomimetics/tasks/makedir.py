# TODO: makedir -> ProjectManagement
import os
import shutil
import glob

# TODO: See set_up_build_directory.py
def setup_natural_directory(simulation_workdir):
    """
    Create 'natural' directory with subdirectories for different stages if it does not exist.
    """
    natural_dir = os.path.join(simulation_workdir, "natural")
    if not os.path.exists(natural_dir):
        os.makedirs(natural_dir)
        subdirs = ["1_leap", "2_min", "3_md", "4_gbsa"]
        for subdir in subdirs:
            os.makedirs(os.path.join(natural_dir, subdir))


def copy_files_and_create_structure(glycomimetic_output_dir, simulation_workdir):
    """
    Process ligand files, check for clash files, and copy to appropriate directory structure in simulation workdir.
    """
    os.chdir(glycomimetic_output_dir)
    for ligand_file in glob.glob("*_ligand.pdb"):
        base_name = ligand_file.replace("_ligand.pdb", "")
        clash_file_pattern = f"*{base_name}*clash*"
        clash_files = glob.glob(clash_file_pattern)

        if clash_files:
            print(
                f"{ligand_file} is too large to fit in the binding site. Won't run it through MD"
            )
            continue

        if ligand_file.startswith("natural"):
            directory_name = base_name
        else:
            directory_name = f"analog_{base_name}"

        full_path = os.path.join(simulation_workdir, directory_name)
        os.makedirs(full_path, exist_ok=True)
        subdirs = ["1_leap", "2_min", "3_md", "4_gbsa"]
        for subdir in subdirs:
            os.makedirs(os.path.join(full_path, subdir), exist_ok=True)

        # Copy files
        shutil.copy(ligand_file, os.path.join(full_path, "1_leap"))
        receptor_file = f"{base_name}_receptor.pdb"
        log_file = f"{base_name}_pdb2glycam.log"
        if os.path.exists(receptor_file):
            shutil.copy(receptor_file, os.path.join(full_path, "1_leap"))
        if os.path.exists(log_file):
            shutil.copy(log_file, os.path.join(full_path, "1_leap"))

        # Remove CONECT lines from pdb file
        with open(ligand_file, "r") as file:
            lines = file.readlines()
        with open(
            os.path.join(full_path, "1_leap", f"{base_name}_ligand_noconect.pdb"), "w"
        ) as file:
            file.writelines([line for line in lines if not line.startswith("CONECT")])


def execute(glycomimetic_output_dir, simulation_workdir):
    """
    Main function to orchestrate directory setup and file processing.
    """
    setup_natural_directory(simulation_workdir)
    copy_files_and_create_structure(glycomimetic_output_dir, simulation_workdir)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py <glycomimetic_output_dir> <simulation_workdir>")
    else:
        execute(sys.argv[1], sys.argv[2])
