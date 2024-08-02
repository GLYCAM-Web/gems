from pathlib import Path

from gemsModules.systemoperations import filesystem_ops
from gemsModules.systemoperations.environment_ops import (
    is_GEMS_live_swarm,
    get_default_GEMS_procs,
)

from gemsModules.deprecated.common import logic as commonlogic
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(
    protocol_files_dir: str,
    output_dir_path: str,
    parm7_real_name: str,
    # uniminimized_parm7_real_name: str,
    rst7_real_name: str,
    # NOTE: Run_Multi-Part_Protocol.bash depends on these precise default names:
    # TODO: Pass from current MdProject
    parm7_protocol_name: str = "MdInput.parm7",
    rst7_protocol_name: str = "MdInput.rst7",
    unsolvated_parm7_file_name: str = "MD_unsolvated.parm7",
):
    log.debug("set_up_run_md_directory.py execute() called, %s", locals())
    
    # ensure that the protocol files directory exists
    if filesystem_ops.directory_exists(protocol_files_dir) == False:
        raise Exception(
            "Protocol files directory does not exist: " + protocol_files_dir
        )

    filesystem_ops.check_make_directory(output_dir_path)
    filesystem_ops.copy_all_files_from_dir_A_to_dir_B(
        A=protocol_files_dir, B=output_dir_path
    )

    # make symbolic link from the expected protocol file names to the real file names
    commonlogic.make_relative_symbolic_link(
        path_down_to_source=f"{output_dir_path}/{parm7_real_name}",
        path_down_to_dest_dir=output_dir_path,
        dest_link_label=parm7_protocol_name,
        parent_directory=output_dir_path,
    )

    commonlogic.make_relative_symbolic_link(
        path_down_to_source=f"{output_dir_path}/{rst7_real_name}",
        path_down_to_dest_dir=output_dir_path,
        dest_link_label=rst7_protocol_name,
        parent_directory=output_dir_path,
    )

    # This file comes from a Sequence project.
    # Let's make a symlink in the directory from unminimized-gas.parm7 to MD_unsolvated.parm7
    if (Path(output_dir_path) / "unminimized-gas.parm7").exists():
        commonlogic.make_relative_symbolic_link(
            path_down_to_source=f"{output_dir_path}/unminimized-gas.parm7",
            path_down_to_dest_dir=output_dir_path,
            dest_link_label=unsolvated_parm7_file_name,
            parent_directory=output_dir_path,
        )
    else:
        # We would like to add a notice here too.
        log.info(
            "unminimized-gas.parm7 does not exist in the protocol files directory. Skipping symlink creation."
        )

    # or maybe? deprecated.common.getGemsExecutionContext???
    if not is_GEMS_live_swarm():
        out_dir = Path(output_dir_path)

        # cp the Local_Run_Parameters.bash.example to Local_Run_Parameters.bash
        # We only do this for test workflows for now because in production the Run_Parameters are set globally.
        # TODO: Amber/MDaaS need to be able to configure this
        src = out_dir / "Local_Run_Parameters.bash.example"
        dest = out_dir / "Local_Run_Parameters.bash"
        filesystem_ops.copy_file_from_A_to_B(A=src, B=dest)

        # now update the Local_Run_Parameters.bash file with the correct number of processors
        filesystem_ops.replace_bash_variable_in_file(
            dest, {"numProcs": get_default_GEMS_procs()}
        )
