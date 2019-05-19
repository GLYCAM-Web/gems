#!/usr/bin/env python3

def investigate_gems_setup(command_line):
  import sys
  import os
  import subprocess
  import json
  import importlib
  from io import StringIO
  GemsHomeNotSet=101
  PythonPathHasNoGemsModules=102
  IncorrectNumberArgs=201
  BadArguments=202
  NotAFile=203
  NotAJSONFile=204

  # check the command line
  if len(command_line) != 2:
    print('Must supply exactly 1 argument.')
    print('%d arguments are supplied'%(len(command_line)-1) )
    sys.exit(IncorrectNumberArgs)

  # check that the argument is a file
  if not os.path.isfile(sys.argv[1]):
    print("The given argument is not a file.  Exiting.")
    sys.exit(NotAFile)

  # check that it contains a json object (see below for schema check)
  try:
    json_object = json.load(open(sys.argv[1],'r'))
  except ValueError:
    print("The given file appears not to be in JSON format.  Exiting.")
    sys.exit(NotAJSONFile)

  # check the paths and modules
  if importlib.util.find_spec("gemsModules") is None:
    print("""
Something is wrong in your Setup.  Investigating.
""")
    print("""
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

  # TODO:  check that the file in argv[1] conforms to our schema



def main():
  import sys,os
  investigate_gems_setup(sys.argv)


if __name__ == "__main__":
  main() 
