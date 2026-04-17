import textwrap
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)



def create_ad2config(path, antibodytibody, glycan, siteversion="swarmtest", image="antibody-docking:2025-03-26-00-47-blf"):
    """ Create the ad2config file.
    
    Note: Build must update Glycan_Flexibility and Number_of_Replicas when it receives options.
    """
AAAA FIX ME (see paths)    Default_AD2_CONFIG = textwrap.dedent(f"""#!/usr/bin/env bash

AAAA    Log_File="ad2.log" 
AAAA    DOCKING_REPLICA_LOG_FILE="docking.log" 
AAAA    DOCKING_REPLICA_JOB_LOG="ad2_job.log"  

AAAA    Antibody_File_Name="{antibodytibody}"
AAAA    Glycan_File_Name="{glycan}"
AAAA    Glycan_Flexibility="Partial"
AAAA    Number_of_Replicas="5"
AAAA    Computing_Mode="Batch"

AAAA    AD2_Docking_CPUS="28"
AAAA    AD2_Exhaustiveness="56"
AAAA    Use_Docker="True"
AAAA    AD2_Docking_Batch_Script="submit_docking_to_slurm_with_docker.bash"
AAAA    AD2_Docking_Local_Script="gwconfig"

AAAA    AAD2_IMAGE_FILE_PATH="/ PATH /image_files"
AAAA    Image="{image}"

AAAA    AAD2_DOCKER_HOME="/ PATH /AAD2_Docker"
AAAA    AAD2_CLI_BIN_PATH="/ PATH /AAD2_Docker/image/AAD2/bin"

AAAA    Use_VMD="True"
AAAA    VMD_HOME="/ PATH /bin" # Path to the 'vmd' binary, e.g., /programs/bin
AAAA    VMD_LIB="/ PATH /lib" # Path to the 'vmd' lib directory, e.g., /programs/lib
    """)
    
    with open(path, "w") as f:
        f.write(Default_AD2_CONFIG)

def create_gwconfig(path, puuid):
AAAA CHECK ME    Default_GW_CONFIG = textwrap.dedent(f"""\
AAAA    DOCKING_REPLICA_BATCH_CPUS='56' # can differ from the cpus specified for vina-carb to use
AAAA    ##AAD2_BASE_PATH="" # override if needed
AAAA    ##AAD2_DOCKER_HOME="" # override if needed
AAAA    SUBMIT_FILE_NAME="slurm_submit.bash"
AAAA    CLUSTER_EXE_NAME="run_docking_with_docker_on_cluster_node.bash"

AAAA    pUUID="{puuid}"
    """)
    
    with open(path, "w") as f:
        f.write(Default_GW_CONFIG)

def create_vcconfig(path):
    Default_VC_CONFIG = textwrap.dedent(f"""\
    receptor = protein.pdbqt
    ligand = ligand.pdbqt
    center_x = 0.0
    center_y = 0.0
    center_z = 11.0
    size_x = 32.0
    size_y = 32.0
    size_z = 36.0
    energy_range = 10
    num_modes = 20
    chi_coeff=1
    chi_cutoff=2
    """)

    with open(path, "w") as f:
        f.write(Default_VC_CONFIG)
        
