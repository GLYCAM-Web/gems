from gemsModules.systemoperations.filesystem_ops import get_current_working_directory
from gemsModules.systemoperations.filesystem_ops import build_filesystem_path
from gemsModules.systemoperations.filesystem_ops import copy_all_files_from_dir_A_to_dir_B

here = get_current_working_directory()
Dir_A = build_filesystem_path( here, "inputs", "A" )
Dir_B = build_filesystem_path( here, "outputs", "B" )

copy_all_files_from_dir_A_to_dir_B(Dir_A, Dir_B)



