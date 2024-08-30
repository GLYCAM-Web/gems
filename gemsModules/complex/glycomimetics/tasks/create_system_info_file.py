from pathlib import Path

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)

def execute(project_dir: Path):
    """
    
    Ex. From Harper host:
    ```    
    installPath=/programs/glycomimeticsWebtool
    AMBERHOME=/cm/shared/apps/amber20/
    GEMSHOME=/programs/gems/yao
    ```
    """
    
    log.debug(f"Creating system info file in {project_dir}")
    
    system_info_file = project_dir / "systemInfo.txt"
    
    # Note: Only valid on Harper at the moment.
    with open(system_info_file, 'w') as f:
        f.write("installPath=/programs/glycomimeticsWebtool\n")
        f.write("AMBERHOME=/cm/shared/apps/amber20/\n")
        f.write("GEMSHOME=/programs/gems/yao\n")
    
    return system_info_file