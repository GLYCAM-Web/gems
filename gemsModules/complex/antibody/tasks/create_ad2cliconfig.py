import os
from gemsModules.systemoperations.filesystem_ops import copy_file_from_A_to_B, replace_bash_variable_in_file

#GEMSHOME = os.environ.get("GEMSHOME")/External/AAD2
EXAMPLE_FILE = f"/programs/website_aad2/test/AAD2_Docker/image/AAD2/99.cluster_utilities/ad2cliconfig.example"


def execute(workdir):
    pUUID = workdir.split("/")[-1]

    # first copy example file to workdir
    project_config_path = copy_file_from_A_to_B(EXAMPLE_FILE, f"{workdir}/ad2cliconfig")
        
    # then replace bash variables in the file
    replacements = {
        "USER_AB_FILEPATH": f"{workdir}/protein.pdb",
        "USER_G_FILEPATH": f"{workdir}/ligand.pdb",
        "AD2CFG_FILEPATH": f"{workdir}/ad2config",
        "WD": workdir,
        "CONTAINER_NAME_PREFIX": f"AntibodyDocking-{pUUID}"
        }
    replace_bash_variable_in_file(project_config_path, replacements)
    
    return project_config_path