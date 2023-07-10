from gemsModules.systemoperations import filesystem_ops
from gemsModules.deprecated.common import logic as commonlogic


def execute(
    protocol_files_dir: str,
    output_dir_path: str,
    uploads_dir_path: str,
    parm7_real_name: str,
    rst7_real_name: str,
    parm7_protocol_name: str = "mdInput.parm7",
    rst7_protocol_name: str = "mdInput.rst7",
):
    # ensure that the protocol files directory exists
    if filesystem_ops.directory_exists(protocol_files_dir) == False:
        raise Exception(
            "Protocol files directory does not exist: " + protocol_files_dir
        )
    # check that the output directory exists, if not, create it
    filesystem_ops.check_make_directory(output_dir_path)
    # copy the protocol files to the output directory
    filesystem_ops.copy_all_files_from_dir_A_to_dir_B(
        A=protocol_files_dir, B=output_dir_path
    )
    # copy the parm7 and rst7 files to the output directory
    fileA = uploads_dir_path + "/" + parm7_real_name
    fileB = output_dir_path + "/" + parm7_real_name
    filesystem_ops.copy_file_from_A_to_B(A=fileA, B=fileB)
    filesystem_ops.copy_file_from_A_to_B(
        A=uploads_dir_path + "/" + rst7_real_name,
        B=output_dir_path + "/" + rst7_real_name,
    )
    # make symbolid links from the expected protocol file names to the real protocol file names
    commonlogic.make_relative_symbolic_link(
        path_down_to_source=output_dir_path + "/" + parm7_real_name,
        path_down_to_dest_dir=output_dir_path,
        dest_link_label=parm7_protocol_name,
        parent_directory=output_dir_path,
    )
    commonlogic.make_relative_symbolic_link(
        path_down_to_source=output_dir_path + "/" + rst7_real_name,
        path_down_to_dest_dir=output_dir_path,
        dest_link_label=rst7_protocol_name,
        parent_directory=output_dir_path,
    )
