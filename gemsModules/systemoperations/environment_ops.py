#!/usr/bin/env python3
import os, sys
import importlib
import traceback

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def get_gems_path() -> str:
    from gemsModules.configuration.user_config import get_effective_gemshome
    path = get_effective_gemshome()
    if not os.path.exists(path):
        log.warning("The current GEMSHOME does not exist: " + str(path))
    return path


def gemsModules_is_findable() -> bool:
    if importlib.util.find_spec("gemsModules") is None:
        return True
    else:
        return False

def find_instance_config() -> str:
    from gemsModules.configuration.user_config import get_effective_instance_config_path
    return get_effective_instance_config_path()


def activate_gems_venv(file_path: str = None) -> None:
    """
    Detects if a virtual environment exists in GEMSHOME, user config, or .gemsrc.
    If present and not running in a container,
    sets VIRTUAL_ENV, prepends .venv/bin to PATH for subprocesses, and re-executes.
    """
    if os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv"):
        # Container environment already has required dependencies installed globally
        return

    from gemsModules.configuration.user_config import get_effective_gemshome, get_effective_venv_path

    # Check for user-configured venv
    custom_venv = get_effective_venv_path()
    if custom_venv and os.path.isdir(custom_venv):
        venv_dir = custom_venv
    else:
        gems_home = get_effective_gemshome()
        venv_dir = os.path.join(gems_home, ".venv")

    if os.path.isdir(venv_dir):
        venv_bin = os.path.join(venv_dir, "bin")
        if venv_bin not in os.environ.get("PATH", "").split(os.pathsep):
            os.environ["PATH"] = venv_bin + os.pathsep + os.environ.get("PATH", "")
        os.environ["VIRTUAL_ENV"] = venv_dir

        venv_python = os.path.join(venv_bin, "python")
        if os.path.exists(venv_python) and not sys.prefix.startswith(venv_dir):
            if os.environ.get("_GEMS_VENV_ACTIVATED") != "1":
                os.environ["_GEMS_VENV_ACTIVATED"] = "1"
                os.execv(venv_python, [venv_python] + sys.argv)



def get_site_version() -> str:
    GW_DOMAIN = os.getenv("GW_DOMAIN") or ""
    GW_DOMAIN = GW_DOMAIN.lower().strip()
    log.debug(f"GW_DOMAIN is: {GW_DOMAIN}")
    
    site_version = "test"
    if "dev" in GW_DOMAIN:
        site_version = "dev"
    elif "test" in GW_DOMAIN:
        site_version = "test"
    elif "swarmtest" in GW_DOMAIN:
        site_version = "swarmtest"
    elif "glycam.org" == GW_DOMAIN:
        site_version = "actual"
 
    log.debug(f"Site version is: {site_version}")
    return site_version
        


def add_gems_to_python_path() -> None:
    GemsPath = get_gems_path()
    sys.path.append(GemsPath)

def getGemsExecutionContext() :
    log.info("getGemsExecutionContext was called.")
    # Currently, if this variable is set to anything at all, GEMS is
    # probably operating in support of a wabsite.
    if 'GW_LIVE_SWARM' in os.environ :
        log.debug("GW_LIVE_SWARM is defined in the current environment.  Assuming this is a website.")
        return 'website'
    else :
        log.debug("GW_LIVE_SWARM is NOT defined in the current environment.  Assuming this is not a website.")
        return 'default'



def getGemsEnvironmentForceSerialExecution() :
    log.info("getGemsEnvironmentForceSerialExecution was called.")
    # Currently, if this variable is set to anything at all, GEMS is
    # probably operating in support of a wabsite.
    if 'GEMS_FORCE_SERIAL_EXECUTION' in os.environ :
        log.debug("GEMS_FORCE_SERIAL_EXECUTION is defined in the current environment.")
        return os.environ.get('GEMS_FORCE_SERIAL_EXECUTION')
    else :
        log.debug("GEMS_FORCE_SERIAL_EXECUTION is NOT defined in the current environment.")
        return 'unset'


def is_GEMS_live_swarm() -> bool:
    """For deciding if DevEnv or not.

    This is different from getGemsExecutionContext in that it returns false if unset.

    TODO: merge with procedural options or deprecate.
    """
    try:
        LIVE_SWARM = os.path.exists(os.path.join(get_gems_path(), "..", "..", "LIVE_SWARM"))
        log.debug("got LIVE_SWARM and it is:  " + str(LIVE_SWARM))
    except Exception as error:
        log.error("Cannnot determine swarm status.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
    finally:
        return LIVE_SWARM


def get_GEMS_test_workflow_steps() -> str:
    try:
        GEMS_MD_TEST_WORKFLOW = os.getenv("GEMS_MD_TEST_WORKFLOW", "False")
        log.debug("got GEMS_MD_TEST_WORKFLOW and it is:  " + str(GEMS_MD_TEST_WORKFLOW))
    except Exception as error:
        log.error("Cannnot determine workflow status.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
    finally:
        if GEMS_MD_TEST_WORKFLOW.lower() in ["true", "yes"]:
            return 2
        elif GEMS_MD_TEST_WORKFLOW.isdigit():
            return int(GEMS_MD_TEST_WORKFLOW)
        else:
            return 0

def is_GEMS_test_workflow() -> bool:
    steps = get_GEMS_test_workflow_steps()
    if steps:
        return True
    else:
        return False
    
    
def get_default_GEMS_procs() -> int:
    """Not robust. Currently recycles GEMSMAKEPROCS environment variable."""
    return int(os.getenv("GEMSMAKEPROCS", 1))


## Return Codes and their associated briefs and messages
## If returning to a shell, we add 128 because the error is fatal
brief_to_code = {
    "GemsHomeNotSet": 1,
    "PythonPathHasNoGemsModules": 2,
    "IncorrectNumberOfArgs": 3,
    "UnknownError": 4,
    "NotAFile": 5,
    "NotAJSONObject": 6,
}
code_to_message = {
    1: "Unable to read or set a usable GEMSHOME.",
    2: "Unable to find gemsModules in the PYTHON_PATH.",
    3: "The number of command-line arguments is incorrect.",
    4: "There was an unknown fatal error.",
    5: "The name specified on the command line does not reference a file.",
    6: "The input supplied is not a JSON objct.",
}


def JSON_Error_Response(errorcode):
    # to get the key if you have the value
    # brief=list(my_dict.keys())[list(my_dict.values()).index(112)])
    theBrief = list(brief_to_code.keys())[list(brief_to_code.values()).index(errorcode)]
    thereturn = (
        '{\n\
    "entity" :\n\
    {\n\
        "type": "CommonServices",\n\
        "responses" :\n\
        [\n\
            { "fatalError" :\n\
                { \n\
                                    "respondingService" : "Utilities",\n\
                                    "notice" : \n\
                                    {\n\
                                        "type" : "Exit",\n\
                                        "code" : "'
        + str(errorcode)
        + '",\n\
                                        "brief" : "'
        + theBrief
        + '",\n\
                                        "message" : "'
        + str(code_to_message[errorcode])
        + '"\n\
                                    }\n\
                                }\n\
            }\n\
        ]\n\
    }\n\
}'
    )
    return thereturn
