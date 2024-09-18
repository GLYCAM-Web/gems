from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Build_Inputs, Build_Outputs
from ...tasks import create_gm_input_file, run_all_glyco, create_system_info_file


log = Set_Up_Logging(__name__)

ic = InstanceConfig()
# https://github.com/GLYCAM-Web/glycomimeticsWebtool/tree/main/internal
GlycoWebtool_path = Path("/programs/glycomimeticsWebtool")


def execute(inputs: Build_Inputs) -> Build_Outputs:
    service_outputs = Build_Outputs(pUUID=inputs.pUUID)

    # Normally the Project builds this path. TODO: better helper 
    project_dir = Path(ic.get_filesystem_path(app="Glycomimetics")) / inputs.pUUID
    if not project_dir.exists():
        log.debug(f"Warning: Project directory {project_dir} does not exist at time of Build_Selected_Positions.")
        raise RuntimeError("No project directory found, cannot run Glycomimetics/Build_Selected_Positions")
    else:
        # TODO/Maybe: Copy the scripts into the project directory.
        # os.system(f"cp -r {GlycoWebtool_path}/scripts {project_dir}")
    
        # Create the input.txt for the Glycomimetics service.
        # Note: We only allow one Selected Position at a time in the API for now.
        create_gm_input_file.execute(inputs.Selected_Modification_Options.Position, project_dir)
        
        # Create the systemInfo.txt
        create_system_info_file.execute(project_dir)
    
        # Run glycomimetics
        run_all_glyco.execute(project_dir, GlycoWebtool_path)


    service_outputs.projectDir = str(project_dir)
    
    return service_outputs
