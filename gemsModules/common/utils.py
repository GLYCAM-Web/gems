#!/usr/bin/env python3

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

def JSON_Error_Response(errorcode):
# to get the key if you have the value
#brief=list(my_dict.keys())[list(my_dict.values()).index(112)])
    theBrief=list(brief_to_code.keys())[list(brief_to_code.values()).index(errorcode)]
    thereturn = "{\n\
	\"entity\" :\n\
	{\n\
		\"type\": \"CommonServices\",\n\
		\"responses\" :\n\
		[\n\
			{ \"fatalError\" :\n\
				{ \n\
                                    \"respondingService\" : \"Utilities\",\n\
                                    \"notice\" : \n\
                                    {\n\
                                        \"type\" : \"Exit\",\n\
                                        \"code\" : \"" + str(errorcode) + "\",\n\
                                        \"brief\" : \"" + theBrief + "\",\n\
                                        \"message\" : \"" + str(code_to_message[errorcode]) + "\"\n\
                                    }\n\
                                }\n\
			}\n\
		]\n\
	}\n\
}"
    return thereturn

def gems_environment_verbosity():
    ## check to see if there is a verbosity set
    ##
    ##  Verbosity meaning suggestions:
    ##  -1  just be quiet and don't even complain about problems
    ##      (use this for JSON-only interactions)
    ##   0  Only give the really important details
    ##   1  Tell a little about what's going on
    ##   2  Give all the gory details you've got
    import sys,os
    GemsDebugVerbosity = os.environ.get('GEMS_DEBUG_VERBOSITY')
    if GemsDebugVerbosity != None:
        return int(GemsDebugVerbosity)
    else:
        return '-1'

def check_gems_home():
    import sys, os
    import importlib
    returnCode = 0
    verbosity=gems_environment_verbosity()
    # check the paths and modules
    if importlib.util.find_spec("gemsModules") is None:
        if verbosity >= 0:
            print("""
Something is wrong in your Setup.  Investigating.

""")
        GemsPath = os.environ.get('GEMSHOME')
        if GemsPath == None:
            this_dir, this_filename = os.path.split(__file__)
            if verbosity >= 0:
                print("""

    GEMSHOME environment variable is not set.

    Set it using somthing like:

      BASH:  export GEMSHOME=/path/to/gems
      SH:    setenv GEMSHOME /path/to/gems

   I'll exit now.

""")
                sys.exit(brief_to_code['GemsHomeNotSet']+128)
            else:
                returnCode = brief_to_code['GemsHomeNotSet'] 
        else:
            if verbosity >= 1:
                print("""
GEMSHOME is set.  This is good.
Trying now to see if adding it to your PYTHONPATH will help.
Also importing gemsModules.
""")
            sys.path.append(GemsPath)
            import gemsModules
            if importlib.util.find_spec("gemsModules") is None:
                if verbosity >= 0:
                    print("""
That didn't seem to work, so I'm not sure what to do.  Exiting.
""")
                    sys.exit(brief_to_code['PythonPathHasNoGemsModules']+128)
                else:
                    returnCode = brief_to_code['PythonPathHasNoGemsModules'] 
            else:
                if verbosity >= 1:
                    print("""
That seems to have worked, so I'm sending you on your way.

In the future, set your PYTHONPATH to include GEMSHOME to
avoid seeing this message.

Bt the way, if your PYTHONPATH contains GEMSHOME, you might not
need GEMSHOME to also be set.

""")
    return returnCode


def JSON_from_stdin(command_line):
    import sys, select, json
    verbosity=gems_environment_verbosity()
    # check if there is standard input 
    if select.select([sys.stdin,],[],[],0.0)[0]:
        jsonObjectString = sys.stdin.read().replace('\n', '')
        # check that it contains a json object 
        try:
            testString = json.loads(jsonObjectString)
        except ValueError:
            if verbosity >= 0:
                print("The content of stdin appears not to be in JSON format.  Exiting.")
                sys.exit(brief_to_code['NotAJSONObject']+128)
            else:
                return brief_to_code['NotAJSONObject']
    else:
        jsonObjectString = None
    return jsonObjectString


def JSON_from_filename_on_command_line(command_line):
    import sys, os, json
    from io import StringIO
    verbosity=gems_environment_verbosity()
    # check the command line
    if len(command_line) != 2:
        if verbosity >= 0:
            print('When reading JSON from a file, you must supply exactly 1 filename as argument.')
            print('%d arguments are supplied'%(len(command_line)-1) )
            sys.exit(brief_to_code['IncorrectNumberOfArgs']+128) 
        else:
            return brief_to_code['IncorrectNumberOfArgs'] 
    # check that the argument is a file
    if not os.path.isfile(sys.argv[1]):
        if verbosity >= 0:
            print("The given argument is not a file.  Exiting.")
            sys.exit(brief_to_code['NotAFile']+128)
        else:
            return brief_to_code['NotAFile']
    else:
        #jsonObjectString = open(sys.argv[1],'r')
        with open(sys.argv[1], 'r') as content_file:
            jsonObjectString = content_file.read()
        # check that it contains a json object 
        try:
            testString = json.loads(jsonObjectString)
        except ValueError:
            if verbosity >= 0:
                print("The given file appears not to be in JSON format.  Exiting.")
                sys.exit(brief_to_code['NotAJSONObject']+128)
            else:
                return brief_to_code['NotAJSONObject']
    return jsonObjectString

# TODO:  check that the file in argv[1] or stdin conforms to our schema

def JSON_From_Command_Line(command_line):
    verbosity=gems_environment_verbosity()
    exitcode=check_gems_home()
    if exitcode > 0 :  # if there was some low-level issue with GEMS or Python
        return JSON_Error_Response(exitcode)
    # Try first to see if there is a JSON object in stdin
    jsonObjectString=JSON_from_stdin(command_line)
    if jsonObjectString is not None:   # there was some stdin
        # Check if the stdin was bad by seeing if the function returned an integer
        try:   
            jsonObjectString = int(str(jsonObjectString)) 
        except ValueError:  # if the response wasn't an error integer...
            # assume it is probably valid JSON and return it
            return jsonObjectString  
        # if the last try/except didn't get us out of here, we have an integer
        # make an error report and return
        return JSON_Error_Response(jsonObjectString)
    # Still here?  There was no stdin.
    # Try to get the JSON from the command line
    jsonObjectString=JSON_from_filename_on_command_line(command_line)
    # The last function shouldn't return 'None', but check anyway
    if jsonObjectString is None:   # something has gone horribly wrong
        return JSON_Error_Response(brief_to_code['UnknownError'])
    try:   # again, check to see if the function returned an integer
        jsonObjectString = int(str(jsonObjectString)) 
    except ValueError:  # if the response wasn't an error integer...
        # assume it is probably valid JSON and return it
        return jsonObjectString  
    # Still here?  Return the error 
    return JSON_Error_Response(jsonObjectString)

### finish writing the new version
def main():
    import sys
    verbosity=gems_environment_verbosity()
    print("The verbosity is" , verbosity)
    theJsonObject = JSON_From_Command_Line(sys.argv)
    print("The JSON object is:")
    print(theJsonObject)

if __name__ == "__main__":
    main() 
