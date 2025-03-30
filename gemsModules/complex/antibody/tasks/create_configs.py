import textwrap
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)



def create_ad2config(path, antibodytibody, glycan, siteversion="swarmtest", image="antibody-docking:2025-03-26-00-47-blf"):
    """ Create the ad2config file.
    
    Note: Build must update Glycan_Flexibility and Number_of_Replicas when it receives options.
    """
    Default_AD2_CONFIG = textwrap.dedent(f"""#!/usr/bin/env bash

    Log_File="ad2.log" 
    DOCKING_REPLICA_LOG_FILE="docking.log" 
    DOCKING_REPLICA_JOB_LOG="ad2_job.log"  

    Antibody_File_Name="{antibodytibody}"
    Glycan_File_Name="{glycan}"
    Glycan_Flexibility="Partial"
    Number_of_Replicas="5"
    Computing_Mode="Batch"

    AD2_Docking_CPUS="28"
    AD2_Exhaustiveness="56"
    Use_Docker="True"
    AD2_Docking_Batch_Script="submit_docking_to_slurm_with_docker.bash"
    AD2_Docking_Local_Script="gwconfig"

    AAD2_IMAGE_FILE_PATH="/programs/website_aad2/image_files"
    Image="{image}"

    AAD2_DOCKER_HOME="/programs/website_aad2/{siteversion}/AAD2_Docker"
    AAD2_CLI_BIN_PATH="/programs/website_aad2/{siteversion}/AAD2_Docker/image/AAD2/bin"

    Use_VMD="True"
    VMD_HOME="/programs/website_aad2/bin" # Path to the 'vmd' binary, e.g., /programs/bin
    VMD_LIB="/programs/website_aad2/lib" # Path to the 'vmd' lib directory, e.g., /programs/lib
    """)
    
    with open(path, "w") as f:
        f.write(Default_AD2_CONFIG)

def create_gwconfig(path, puuid):
    Default_GW_CONFIG = textwrap.dedent(f"""\
    DOCKING_REPLICA_BATCH_CPUS='56' # can differ from the cpus specified for vina-carb to use
    ##AAD2_BASE_PATH="" # override if needed
    ##AAD2_DOCKER_HOME="" # override if needed
    SUBMIT_FILE_NAME="slurm_submit.bash"
    CLUSTER_EXE_NAME="run_docking_with_docker_on_cluster_node.bash"

    pUUID="{puuid}"
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
        
def create_vccconfig(path):
    pass