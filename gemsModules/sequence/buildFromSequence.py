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

    detect_sugars PDB_file.pdb

The output goes to standard out (your terminal window, usually).
So, alternately:

    detect_sugars PDB_file.pdb > output_file_name

""")
    sys.exit(1)

# import gems/gmml stuff
sys.path.append(GemsPath)
import gmml

def main():
	thisFileName = sys.argv[0]
	prepFileName = sys.argv[1]
	sequence = sys.argv[2]
	outOffFileName = sys.argv[3]
	outPdbFileName = sys.argv[4]

	print("thisFile: " + thisFileName)
	print("prepFile: " + prepFileName)
	print("sequence: " + sequence)
	print("outOff: " + outOffFileName)
	print("outPdb: " + outPdbFileName)

	prep = gmml.PrepFile(prepFileName)
	assembly = gmml.Assembly()
	assembly.SetName("CONDENSEDSEQUENCE")
	assembly.BuildAssemblyFromCondensedSequence(sequence, prep)
	assembly.CreateOffFileFromAssembly(outOffFileName, 0)
	content = assembly.BuildPdbFileStructureFromAssembly()

	content.Write(outPdbFileName)
	

if __name__ == "__main__":
    main()