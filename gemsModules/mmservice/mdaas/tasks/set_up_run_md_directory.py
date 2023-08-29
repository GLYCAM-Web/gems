from pathlib import Path

from gemsModules.systemoperations import filesystem_ops
from gemsModules.systemoperations.environment_ops import is_GEMS_test_workflow

from gemsModules.deprecated.common import logic as commonlogic
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(
    protocol_files_dir: str,
    output_dir_path: str,
    uploads_dir_path: str,
    parm7_real_name: str,
    rst7_real_name: str,
    parm7_protocol_name: str = "mdInput.parm7",
    rst7_protocol_name: str = "mdInput.rst7",
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
    # copy the parm7 to the output directory
    out_dir = Path(output_dir_path)
    src = Path(parm7_real_name)
    dest = out_dir / src.name
    filesystem_ops.copy_file_from_A_to_B(A=src, B=dest)
    # make symbolic link from the expected protocol file names to the real file names
    commonlogic.make_relative_symbolic_link(
        path_down_to_source=dest,
        path_down_to_dest_dir=output_dir_path,
        dest_link_label=parm7_protocol_name,
        parent_directory=output_dir_path,
    )

    # copy the rst7 to the output directory
    src = Path(rst7_real_name)
    dest = out_dir / src.name
    filesystem_ops.copy_file_from_A_to_B(A=src, B=dest)
    commonlogic.make_relative_symbolic_link(
        path_down_to_source=dest,
        path_down_to_dest_dir=output_dir_path,
        dest_link_label=rst7_protocol_name,
        parent_directory=output_dir_path,
    )

    if is_GEMS_test_workflow():
        # cp the Local_Run_Parameters.bash.example to Local_Run_Parameters.bash
        # TODO: Amber/MDaaS need to be able to configure this
        src = out_dir / "Local_Run_Parameters.bash.example"
        dest = out_dir / "Local_Run_Parameters.bash"
        filesystem_ops.copy_file_from_A_to_B(A=src, B=dest)
