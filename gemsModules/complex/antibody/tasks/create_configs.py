import textwrap
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)



import os
from typing import Optional

def create_ad2config(
    path,
    antibodytibody,
    glycan,
    siteversion=None,
    image=None,
    aad2_config=None,
    aad2_docker_home=None,
    aad2_cli_bin_path=None,
    aad2_image_file_path=None,
    vmd_home=None,
    vmd_lib=None,
):
    """ Create the ad2config file.
    
    Note: Build must update Glycan_Flexibility and Number_of_Replicas when it receives options.
    """
    if aad2_config is None:
        try:
            from gemsModules.configuration.main_api import session_instance_config
            aad2_config = session_instance_config.get_aad2_configuration()
        except Exception:
            pass

    env_docker_home = os.environ.get("AAD2_DOCKER_HOME")
    docker_home = aad2_docker_home or (aad2_config.aad2_docker_home if aad2_config else None) or env_docker_home or ""
    cli_bin = aad2_cli_bin_path or (aad2_config.get_cli_bin_path() if aad2_config else None) or (os.path.join(docker_home, "image/AAD2/bin") if docker_home else "")
    img = image or (aad2_config.get_image() if aad2_config else None) or ""
    img_file_path = aad2_image_file_path or (aad2_config.aad2_image_file_path if aad2_config else None) or (os.path.join(docker_home, "image_files") if docker_home else "")
    vmd_h = vmd_home or (aad2_config.vmd_home if aad2_config else None) or ""
    vmd_l = vmd_lib or (aad2_config.vmd_lib if aad2_config else None) or ""

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

    AAD2_IMAGE_FILE_PATH="{img_file_path}"
    Image="{img}"

    AAD2_DOCKER_HOME="{docker_home}"
    AAD2_CLI_BIN_PATH="{cli_bin}"

    Use_VMD="True"
    VMD_HOME="{vmd_h}"
    VMD_LIB="{vmd_l}"
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
        
