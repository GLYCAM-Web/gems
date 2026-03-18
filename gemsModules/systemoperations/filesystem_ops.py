import os, glob, shutil
from pathlib import Path
from typing import Union, List
import tempfile


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def get_current_working_directory() -> str:
    return os.getcwd()


def build_fs_path(*parts: str) -> str:
    return str(Path(*parts))


def build_filesystem_path(*path_parts: str):
    """Builds an operating-system-specific path string from its parts as strings."""
    log.info("build_filesystem_path was called")
    log.debug("The path parts are: ")
    log.debug(path_parts)
    try:
        the_path = ""
        for x in path_parts:
            the_path = os.path.join(the_path, x)
        log.debug("The final path is:  >>>" + str(the_path) + "<<<")
        return the_path
    except Exception as e:
        log.error("build_filesystem_path failed with the following error:")
        log.error(e)
        raise RuntimeError


def directory_exists(Dir_Path: str) -> bool:
    return os.path.isdir(Dir_Path)


def make_directory(Dir_Path: str):
    os.mkdir(Dir_Path)


def check_make_directory(Dir_Path: str):
    Path(Dir_Path).mkdir(parents=True, exist_ok=True)


def separate_path_and_filename(File_Path: str) -> tuple[str, str]:
    this_dir, this_filename = os.path.split(File_Path)
    return this_dir, this_filename


def check_if_files_exist(paths: list, parent_dir: str = None, return_found: bool = False, any_exist: bool = False) -> Union[List, bool]:
    """Check if files exist in the given paths.

    Args:
        paths (list): List of file paths to check.
        parent_dir (str): Parent directory to check for files. If None, check the paths directly.
                            If not None, the paths will be joined with the parent directory.
        return_found (bool): If True, return the list of found files. If False, return True if all files exist, otherwise False.
        any_exist (bool): If True, return True if any file exists, otherwise False if any file is missing.
    
    Returns:
        list | bool: List of found files if return_found is True, otherwise True if all files exist, otherwise False.
    """
    if parent_dir is not None:
        paths = [os.path.join(parent_dir, path) for path in paths]
        
    found = []
    for path in paths:
        if os.path.exists(path):
            found.append(path)
            
    if return_found:
        return found
    if any_exist:
        return len(found) > 0
    else:
        return len(found) == len(paths)


def copy_file_from_A_to_B(A: str, B: str):
    # Make me more resilient one day
    log.info(f"copy_file_from_A_to_B was called with A={A} and B={B}.")
    return shutil.copy(A, B)


def copy_all_files_from_dir_A_to_dir_B(
    A: str, B: str, follow_symlinks=True, copymode=shutil.copy
):
    log.info("copy_all_files_from_dir_A_to_dir_B was called.")
    log.debug("Directory A (source) is: " + str(A))
    log.debug("Directory B (destination) is: " + str(B))
    log.debug("follow_symlinks is :" + str(follow_symlinks))
    log.debug("The copy mode is:")
    log.debug(copymode)
    check_make_directory(B)
    try:
        src_files = build_filesystem_path(A, "*")
        for file in glob.glob(src_files):
            log.debug(file)
            copymode(file, B)
    except Exception as e:
        log.error("Unable to copy files from " + str(A) + " to " + str(B) + ".")
        log.error("Here is the exception:")
        log.error(e)
        raise RuntimeError


def copy_all_files_from_dir_A_to_dir_B_preserve_metadata(
    A: str, B: str, follow_symlinks=True
):
    log.info("copy_all_files_from_dir_A_to_dir_B_preserve_metadata was called.")
    copy_all_files_from_dir_A_to_dir_B(A, B, follow_symlinks, copymode=shutil.copy2)


def copy_dir_A_to_become_dir_B():
    pass


def copy_dir_A_inside_of_dir_B():
    pass


def replace_bash_variable_in_file(path, vars: dict[str, any]):
    """Replace a value for a bash script variable. Only works in the simplest cases."""
    # a bash var is usually set like this:  varname="varvalue"
    # so we need to replace the varname= with varname="varvalue"
    # we also need to make sure that the varvalue is quoted
    # first find the line in question
    # then split the line into two parts
    modified = False
    with open(path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        # Just to be safe, we're not interested in lines that start with "if"
        # might as well skip comments too
        if line.strip().startswith("if") or line.startswith("#"):
            continue

        if line.startswith("export"):
            line = line[7:]
        for vname, vval in vars.items():
            if f"{vname}=" in line:
                log.debug(f"Found {vname} in {line}")
                old_val = line.split("=")[1]
                lines[i] = line.replace(old_val, f"'{vval}'\n")
                modified = True

    if modified:
        # write back lines
        with open(path, "w") as f:
            f.writelines(lines)
            return True


def is_directory_writable(directory_path, make_if_needed:bool = False):
    """Checks if a directory is writable by attempting to create a temporary file."""
    try:
        # If directory does not exist, and if asked to do so, try to make the directory:
        if make_if_needed:
            check_make_directory(directory_path)
        # Create a temporary file in the directory
        with tempfile.TemporaryFile(dir=directory_path) as temp_file:
            # Try writing to the file
            temp_file.write(b"test write")
        return True
    except PermissionError:
        return False
    except FileNotFoundError:
        # Parent directory does not exist
        return False
    except OSError as e:
        # Catch other potential OS errors (e.g., full disk, specific Windows issues)
        print(f"An OS error occurred: {e}")
        return False


def write_string_to_file(theString, filePath, writeMode : str = 'w'):
    # log.info("writeStringToFile() was called.\n")
    try:
        with open(filePath, writeMode, encoding='utf-8') as file:
           file.write(theString)
    except Exception as error:
        log.error("There was a problem writing the request to file.")
        raise error


