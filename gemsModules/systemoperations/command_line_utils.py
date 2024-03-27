#!/usr/bin/env python3
import json
import os
import sys
import traceback
import select

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


#######      COMMAND LINE RETURN INFO      ########
##                                               ##
## These codes are only for command line use     ##
##
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


def build_error_response_command_line(errorcode: int, isshell: bool = True) -> str:

    theBrief = list(brief_to_code.keys())[list(brief_to_code.values()).index(errorcode)]

    if isshell:
        returnCode = errorcode + 128
    else:
        returnCode = errorcode

    thereturn = json.dumps(
        {
            "entity": {
                "type": "CommonServices",
                "responses": [
                    {
                        "fatalError": {
                            "respondingService": "System Operations",
                            "notice": {
                                "type": "Exit",
                                "code": str(returnCode),
                                "brief": theBrief,
                                "message": str(code_to_message[errorcode]),
                            },
                        }
                    }
                ],
            }
        },
        indent=2,
    )

    return thereturn


def STRING_from_file_named_on_command_line(command_line):
    #    from io import StringIO
    if len(command_line) < 2:
        return None
    if not os.path.isfile(command_line[1]):
        return None
    else:
        with open(command_line[1], "r") as content_file:
            # with open(sys.argv[1], 'r') as content_file:
            return content_file.read()


def STRING_from_stdin(
    standard_input=sys.stdin, initial_timeout=None, extend_timeout=None
) -> str:
    """
    Attempts to read from standard input with a timeout.
    If the initial select times out, the timeout can be extended once.

    Args:
    - standard_input: The input stream to read from. Defaults to sys.stdin.
    - initial_timeout: The initial timeout in seconds.
    - extend_timeout: Optional. An additional amount of time to wait if the initial wait times out.
                      If None, no second attempt is made.

    Returns:
    - The read string if available within the timeout(s), or None if not.
    """
    ready, _, _ = select.select([standard_input], [], [], initial_timeout)
    if ready:
        return standard_input.read()
    elif extend_timeout is not None:
        ready, _, _ = select.select([standard_input], [], [], extend_timeout)
        if ready:
            return standard_input.read()

    return None


def JSON_From_Command_Line(command_line, standard_input) -> tuple[str, int]:
    # Try to get the JSON from the command line
    jsonObjectString = STRING_from_file_named_on_command_line(command_line)

    if jsonObjectString is None:
        # If there is no JSON, try to get it from standard input
        jsonObjectString = STRING_from_stdin(standard_input, 0.0, 0.5)

    # If there is no JSON, return an error
    if jsonObjectString is None:
        return build_error_response_command_line(5), 133

    # If the JSON is not a JSON object, return an error
    try:
        json.loads(jsonObjectString)
    except:
        return build_error_response_command_line(6), 134

    return jsonObjectString, 0
