#!/usr/bin/env python3
import os, sys
import importlib
import traceback

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def get_gems_path() -> str:
    return os.environ.get("GEMSHOME")


def gemsModules_is_findable() -> bool:
    if importlib.util.find_spec("gemsModules") is None:
        return True
    else:
        return False


def add_gems_to_python_path() -> None:
    GemsPath = get_gems_path()
    sys.path.append(GemsPath)


def is_GEMS_test_workflow() -> bool:
    try:
        GEMS_MD_TEST_WORKFLOW = os.getenv("GEMS_MD_TEST_WORKFLOW", False)
        log.debug("got GEMS_MD_TEST_WORKFLOW and it is:  " + str(GEMS_MD_TEST_WORKFLOW))
    except Exception as error:
        log.error("Cannnot determine workflow status.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
    finally:
        return GEMS_MD_TEST_WORKFLOW


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
