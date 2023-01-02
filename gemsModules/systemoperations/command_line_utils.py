#!/usr/bin/env python3
from enum import Enum
import traceback

from gemsModules.common.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def check_gems_home():
    import sys, os
    import importlib
    returnCode = 0
    # check the paths and modules
    if importlib.util.find_spec("gemsModules") is None:
        print("""
Something is wrong in your Setup.  Investigating.

""")
        GemsPath = os.environ.get('GEMSHOME')
        if GemsPath == None:
            this_dir, this_filename = os.path.split(__file__)
            log.error("""

    GEMSHOME environment variable is not set.

    Set it using somthing like:

      BASH:  export GEMSHOME=/path/to/gems
      SH:    setenv GEMSHOME /path/to/gems

   I'll exit now.

""")
            ###   return something instead of this:   sys.exit(1)
        else:
            print("""
GEMSHOME is set.  This is good.
Trying now to see if adding it to your PYTHONPATH will help.
Also importing gemsModules.
""")
            sys.path.append(GemsPath)
            import gemsModules
            if importlib.util.find_spec("gemsModules") is None:
                print("""
That didn't seem to work, so I'm not sure what to do.  Exiting.
""")
                ###   return something instead of this:   sys.exit(1)
            else:
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
    # check if there is standard input 
    if select.select([sys.stdin,],[],[],0.0)[0]:
        jsonObjectString = sys.stdin.read().replace('\n', '')
        # check that it contains a json object 
        try:
            testString = json.loads(jsonObjectString)
        except ValueError:
            log.debug("The content of stdin appears not to be in JSON format.  Exiting.")
            ###   return something instead of this:   sys.exit(1)
    else:
        jsonObjectString = None
    return jsonObjectString


def JSON_from_filename_on_command_line(command_line):
    import sys, os, json
    from io import StringIO
    # check the command line
    if len(command_line) != 2:
        print('When reading JSON from a file, you must supply exactly 1 filename as argument.')
        print('%d arguments are supplied'%(len(command_line)-1) )
        ###   return something instead of this:   sys.exit(1)
    # check that the argument is a file
    if not os.path.isfile(sys.argv[1]):
        print("The given argument is not a file.  Exiting.")
        ###   return something instead of this:   sys.exit(1)
    else:
        #jsonObjectString = open(sys.argv[1],'r')
        with open(sys.argv[1], 'r') as content_file:
            jsonObjectString = content_file.read()
        # check that it contains a json object 
        try:
            testString = json.loads(jsonObjectString)
        except ValueError:
            print("The given file appears not to be in JSON format.  Exiting.")
            ###   return something instead of this:   sys.exit(1)
    return jsonObjectString

# TODO:  check that the file in argv[1] or stdin conforms to our schema

def JSON_From_Command_Line(command_line):
    import sys
    exitcode=check_gems_home()
    if exitcode != 0 :  # if there was some low-level issue with GEMS or Python
        print("could not read json from command line")
        ###   return something instead of this:   sys.exit(1)
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
        print("The content of stdin appears not to be in JSON format.  Exiting.")
        ###   return something instead of this:   sys.exit(1)
    # Still here?  There was no stdin.
    # Try to get the JSON from the command line
    jsonObjectString=JSON_from_filename_on_command_line(command_line)
    # The last function shouldn't return 'None', but check anyway
    if jsonObjectString is None:   # something has gone horribly wrong
        print("The content of stdin appears not to be in JSON format.  Exiting.")
        ###   return something instead of this:   sys.exit(1)
    try:   # again, check to see if the function returned an integer
        jsonObjectString = int(str(jsonObjectString)) 
    except ValueError:  # if the response wasn't an error integer...
        # assume it is probably valid JSON and return it
        return jsonObjectString  
    # Still here?  Return the error 
    print("The content of stdin appears not to be in JSON format.  Exiting.")
    ###   return something instead of this:   sys.exit(1)

### finish writing the new version
def main():
    import sys
    theJsonObject = JSON_From_Command_Line(sys.argv)
    print("The JSON object is:")
    print(theJsonObject)

