from pathlib import Path

from gemsModules.systemoperations.instance_config import InstanceConfig

from .api import Build_Inputs, Build_Outputs

from ...tasks import create_gm_input_file, run_all_glyco, create_system_info_file

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)
ic = InstanceConfig()


def execute(inputs: Build_Inputs) -> Build_Outputs:
    service_outputs = Build_Outputs(pUUID=inputs.pUUID)

    # https://github.com/GLYCAM-Web/glycomimeticsWebtool/tree/main/internal

    project_dir = Path(ic.get_filesystem_path(app="Glycomimetics")) / inputs.pUUID
    if not project_dir.exists():
        log.debug(f"Warning: Project directory {project_dir} does not exist at time of Build_Selected_Positions.")
    else:
        # Note: We only allow one Selected Position at a time in the API for now.
        # The Complex.pdb should already be copied to the project directory by now. By PM service probably.

        # Create the input.txt for the Glycomimetics service.
        create_gm_input_file.execute(inputs.Selected_Modification_Options.Position, project_dir)
        
        # Create the systemInfo.txt
        create_system_info_file.execute(project_dir)
        
        # TODO/Maybe: Copy the scripts into the project directory.
        # If we do this, we need the PM service to do it.
        GlycoWebtool_path = Path("/programs/glycomimeticsWebtool")
        # os.system(f"cp -r {GlycoWebtool_path}/scripts {project_dir}")
        
        # Run glycomimetics
        try:
            run_all_glyco.execute(project_dir, GlycoWebtool_path)
        except Exception as e:
            # append notice
            service_outputs.notices.addNotice(
                Brief="Error running Glycomimetics",
                Scope="Service",
                Messenger="Glycomimetics",
                Type="Error",
                Code="700",
                Message=f"Error running Glycomimetics: {e}",
            )

    service_outputs.projectDir = str(project_dir)
    
    return service_outputs
