import os
from typing import Optional
from gemsModules.systemoperations.filesystem_ops import copy_file_from_A_to_B, replace_bash_variable_in_file


def get_example_file(example_file: Optional[str] = None, aad2_config=None) -> Optional[str]:
    """
    Resolve path to ad2cliconfig.example file using parameter, aad2_config, IC, or AAD2_DOCKER_HOME.
    """
    if example_file:
        return example_file
    if aad2_config is not None:
        cand = aad2_config.get_ad2cliconfig_example_file()
        if cand:
            return cand
    try:
        from gemsModules.configuration.main_api import session_instance_config
        cfg = session_instance_config.get_aad2_configuration()
        if cfg:
            cand = cfg.get_ad2cliconfig_example_file()
            if cand:
                return cand
    except Exception:
        pass

    env_docker_home = os.environ.get("AAD2_DOCKER_HOME")
    if env_docker_home:
        return os.path.join(env_docker_home, "image/AAD2/99.cluster_utilities/ad2cliconfig.example")

    return None


EXAMPLE_FILE = get_example_file()


def execute(workdir, example_file: Optional[str] = None, aad2_config=None):
    pUUID = workdir.split("/")[-1]

    target_example = get_example_file(example_file, aad2_config)
    if not target_example or not os.path.exists(target_example):
        raise FileNotFoundError(
            f"ad2cliconfig example template not found or not configured: {target_example}"
        )

    # first copy example file to workdir
    project_config_path = copy_file_from_A_to_B(target_example, f"{workdir}/ad2cliconfig")
        
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
