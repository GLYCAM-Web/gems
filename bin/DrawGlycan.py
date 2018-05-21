#!/usr/bin/env python3
import sys
import os

# check out the environment
GemsPath = os.environ.get('GEMSHOME')
if GemsPath == None:
    print("""

Must set GEMSHOME environment variable

    BASH:  export GEMSHOME=/path/to/gems
    SH:    setenv GEMSHOME /path/to/gems

""")
    sys.exit(1)

# check out the command line
if len(sys.argv)<2:
    print("""
Usage:

    DrawGlycan.py SEQUENCE

""")
    sys.exit(1)

# import gems/gmml stuff
sys.path.append(GemsPath)
import gmml

sequence = gmml.CondensedSequence(sys.argv[1])

configs = gmml.GraphVizDotConfig()

# If you want to change any of the default values
# for the configs struct now would be the time to
# do it.
# Example:
# configs.dpi = 360

sequence.WriteGraphVizDotFile(configs)
