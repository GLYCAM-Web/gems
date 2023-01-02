import os, glob, shutil
from pathlib import Path


from gemsModules.status.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def get_current_working_directory() -> str :
    return os.getcwd()

def build_filesystem_path(*path_parts : str ):
    """ Builds an operating-system-specific path string from its parts as strings. """
    log.info("build_filesystem_path was called")
    log.debug("The path parts are: ")
    log.debug(path_parts)
    try : 
        the_path = ""
        for x in path_parts :
            the_path = os.path.join(the_path, x)
        log.debug("The final path is:  >>>" + str(the_path) + "<<<")
        return the_path
    except Exception as e :
        log.error("build_filesystem_path failed with the following error:")
        log.error(e)
        raise RuntimeError 


def directory_exists( Dir_Path : str ) -> bool:
    return os.path.isdir(Dir_Path) 

def make_directory( Dir_Path : str ):
    os.mkdir(Dir_Path)

def check_make_directory( Dir_Path : str ):
    Path( Dir_Path ).mkdir( parents=True, exist_ok=True )

def separate_path_and_name_for_file( File_Path : str ) -> ( str , str ) :
    this_dir, this_filename = os.path.split(__file__)
    return this_dir , this_filename


def copy_all_files_from_dir_A_to_dir_B(A : str, B : str, follow_symlinks=True, copymode=shutil.copy) :
    log.info("copy_all_files_from_dir_A_to_dir_B was called.")
    log.debug("Directory A (source) is: " + str(A))
    log.debug("Directory B (destination) is: " + str(B))
    log.debug("follow_symlinks is :" + str(follow_symlinks))
    log.debug("The copy mode is:")
    log.debug(copymode)
    check_make_directory(B)
    try :
        src_files = build_filesystem_path(A , '*')
        for file in glob.glob(src_files):
            log.debug(file)
            copymode(file, B)
    except Exception as e :
        log.error("Unable to copy files from " + str(A) + " to " + str(B) + ".")
        log.error("Here is the exception:")
        log.error(e)
        raise RuntimeError 

def copy_all_files_from_dir_A_to_dir_B_preserve_metadata(A : str, B : str, follow_symlinks=True) :
    log.info("copy_all_files_from_dir_A_to_dir_B_preserve_metadata was called.")
    copy_all_files_from_dir_A_to_dir_B(A , B , follow_symlinks , copymode=shutil.copy2) 


def copy_dir_A_to_become_dir_B() :
    pass

def copy_dir_A_inside_of_dir_B() :
    pass


