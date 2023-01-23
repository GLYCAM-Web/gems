#!/usr/bin/env python3
import json
import os
import sys
import traceback

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


#######      COMMAND LINE RETURN INFO      ########
##                                               ##
## These codes are only for command line use     ##
##
## Return Codes and their associated briefs and messages
## If returning to a shell, we add 128 because the error is fatal

brief_to_code = {
    'GemsHomeNotSet' :              1 ,
    'PythonPathHasNoGemsModules' :  2 ,
    'IncorrectNumberOfArgs' :       3 ,
    'UnknownError' :                4 ,
    'NotAFile' :                    5 ,
    'NotAJSONObject' :              6
}

code_to_message = {
    1 : 'Unable to read or set a usable GEMSHOME.',
    2 : 'Unable to find gemsModules in the PYTHON_PATH.',
    3 : 'The number of command-line arguments is incorrect.',
    4 : 'There was an unknown fatal error.',
    5 : 'The name specified on the command line does not reference a file.',
    6 : 'The input supplied is not a JSON objct.'
}


def build_error_response_command_line(errorcode: int, isshell:bool=True) -> str :
    
    theBrief=list(brief_to_code.keys())[list(brief_to_code.values()).index(errorcode)]
    
    if isshell:
        returnCode = errorcode + 128
    else: 
        returnCode = errorcode

    thereturn = "{\n\
    \"entity\" :\n\
    {\n\
        \"type\": \"CommonServices\",\n\
        \"responses\" :\n\
        [\n\
            { \"fatalError\" :\n\
                { \n\
                                    \"respondingService\" : \"System Operations\",\n\
                                    \"notice\" : \n\
                                    {\n\
                                        \"type\" : \"Exit\",\n\
                                        \"code\" : \"" + str(returnCode) + "\",\n\
                                        \"brief\" : \"" + theBrief + "\",\n\
                                        \"message\" : \"" + str(code_to_message[errorcode]) + "\"\n\
                                    }\n\
                                }\n\
            }\n\
        ]\n\
    }\n\
}"
    return thereturn



def STRING_from_stdin(standard_input) -> str :
    import select
    if select.select([standard_input,],[],[],0.0)[0]:
    #if select.select([sys.stdin,],[],[],0.0)[0]:
        return standard_input.read()
        #return sys.stdin.read()
    else:
        return None


def STRING_from_file_named_on_command_line(command_line):
    #    from io import StringIO
    if len(command_line) < 2:
        return None
    if not os.path.isfile(command_line[1]):
    #if not os.path.isfile(sys.argv[1]):
        return None
    else:
        with open(command_line[1], 'r') as content_file:
        #with open(sys.argv[1], 'r') as content_file:
            return content_file.read()



def JSON_From_Command_Line(command_line, standard_input) -> tuple[str, int]:
    # Try first to see if there is a JSON object in stdin
    jsonObjectString=STRING_from_stdin(standard_input)
    if jsonObjectString is not None:   # there was some stdin
        try:   
            json.loads(jsonObjectString)
        except:  
            return build_error_response_command_line(6), 134
        return jsonObjectString, 0
    # Try to get the JSON from the command line
    jsonObjectString=STRING_from_file_named_on_command_line(command_line)
    if jsonObjectString is None:
        return build_error_response_command_line(5), 133
    try:   
        json.loads(jsonObjectString)
    except:  
        return build_error_response_command_line(6), 134
    return jsonObjectString, 0

