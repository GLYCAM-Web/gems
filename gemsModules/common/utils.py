#!/usr/bin/env python3

def set_errors_and_values():
    GemsHomeNotSet=101
    PythonPathHasNoGemsModules=102
    IncorrectNumberArgs=201
    BadArguments=202
    NotAFile=203
    NotAJSONFile=204

def gems_environment_verbosity():
    ## check to see if there is a verbosity set
    import sys,os
    GemsDebugVerbosity = os.environ.get('GEMS_DEBUG_VERBOSITY')
    if GemsDebugVerbosity != None:
        return GemsDebugVerbosity
    else:
        return 0

def check_gems_home():
    import sys, os
    import importlib
    set_errors_and_values()
    # check the paths and modules
    if importlib.util.find_spec("gemsModules") is None:
        print("""
Something is wrong in your Setup.  Investigating.

Checking if GEMSHOME is set:
""")
        GemsPath = os.environ.get('GEMSHOME')
        if GemsPath == None:
            this_dir, this_filename = os.path.split(__file__)
            print("""

    GEMSHOME environment variable is not set.

    Set it using somthing like:

      BASH:  export GEMSHOME=/path/to/gems
      SH:    setenv GEMSHOME /path/to/gems

   I'll exit now.

""")
            sys.exit(GemsHomeNotSet)
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
                sys.exit(PythonPathHasNoGemsModules)
            else:
                print("""
That seems to have worked, so I'm sending you on your way.

In the future, set your PYTHONPATH to include GEMSHOME to
avoid seeing this message.

Bt the way, if your PYTHONPATH contains GEMSHOME, you might not
need GEMSHOME to also be set.

""")


def JSON_from_stdin(command_line):
    import sys
    import select
    # check if there is standard input 
    if select.select([sys.stdin,],[],[],0.0)[0]:
        #print("Have data!  Here it is!")
        jsonObjectString = sys.stdin.read().replace('\n', '')
        #print(">>>"+jsonObjectString+"<<<")
    else:
        #print("No data")
        jsonObjectString = None
    return jsonObjectString


def JSON_from_filename_on_command_line(command_line):
    import sys, os, json
    set_errors_and_values()

    # check the command line
    if len(command_line) != 2:
        print('When reading JSON from a file, you must supply exactly 1 filename as argument.')
        print('%d arguments are supplied'%(len(command_line)-1) )
        sys.exit(IncorrectNumberArgs)

    # check that the argument is a file
    if not os.path.isfile(sys.argv[1]):
        print("The given argument is not a file.  Exiting.")
        sys.exit(NotAFile)

    # check that it contains a json object 
    try:
        jsonObjectString = json.load(open(sys.argv[1],'r'))
    except ValueError:
        print("The given file appears not to be in JSON format.  Exiting.")
        sys.exit(NotAJSONFile)

    return jsonObjectString


# TODO:  check that the file in argv[1] or stdin conforms to our schema



###
###  Rename me and finish writing me
def investigate_gems_setup(command_line, stdin_ok=False):
  import sys
  import select
  import os
  import subprocess
  import json
  import importlib
  from io import StringIO



### finish writing the new version
def main():
    check_gems_environment_variables()
    verbosity=get_gems_environment_verbosity()
    print("The verbosity is" , verbosity)


if __name__ == "__main__":
    main() 
