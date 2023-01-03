#!/usr/bin/env python3
import json
import os
import sys
import traceback

from gemsModules.status.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def STRING_from_stdin(command_line) -> str :
    import select
    if select.select([sys.stdin,],[],[],0.0)[0]:
        return sys.stdin.read()
    else:
        return None


def STRING_from_filename_on_command_line(command_line):
    #    from io import StringIO
    if len(command_line) < 2:
        return None
    if not os.path.isfile(sys.argv[1]):
        return None
    else:
        with open(sys.argv[1], 'r') as content_file:
            return content_file.read()


def build_error_response_bad_JSON() -> str :
    return "This is a returned error response string.\n"


def JSON_From_Command_Line(command_line) -> (str, int):
    # Try first to see if there is a JSON object in stdin
    jsonObjectString=STRING_from_stdin(command_line)
    if jsonObjectString is not None:   # there was some stdin
        try:   
            jsonObjectDict = json.loads(jsonObjectString)
        except:  
            return build_error_response_bad_JSON(), 129
        return jsonObjectString, 0
    # Try to get the JSON from the command line
    jsonObjectString=STRING_from_filename_on_command_line(command_line)
    try:   
        jsonObjectDict = json.loads(jsonObjectString)
    except:  
        return build_error_response_bad_JSON(), 129
    return jsonObjectString, 0

