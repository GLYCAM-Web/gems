#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path

# check out the environment
GemsPath = os.environ.get('GEMSHOME')
if GemsPath == None:
    print("""

Must set GEMSHOME environment variable

    BASH:  export GEMSHOME=/path/to/gems
    SH:    setenv GEMSHOME /path/to/gems

""")
    sys.exit(1)

# import gems/gmml stuff
sys.path.append(GemsPath)
import gmml

## Defining the Usage Statement
USAGE="""

GlycosylationSiteTable.py [ PDBFILE ] 
PDBFILE:
    The pdb file is read in and stuff happens etc.

"""

## Declare and define the main function.
def main():
    
    assembly = gmml.Assembly(sys.argv[1], gmml.PDB)
    assembly.BuildStructureByDistance(4) # number of threads to use. Needs to go away into assembly constructor.
    assembly.GenerateResidueNodesInAssembly() # This needs to go away into assembly constructor.
    siteFinder = gmml.GlycosylationSiteFinder(assembly)
    print(siteFinder.PrintTable())
    
    sys.exit(0)

## Now we call main function.
if __name__ == "__main__":
    main()
