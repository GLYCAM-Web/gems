#!/usr/bin/python3.4

import sys
import os

###  Make sure the gems/gmml environment is set

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
#sys.path.insert(0, '/programs/repos/gems/')
#sys.path.insert(0, GemsPath)
sys.path.append(GemsPath)

import gmml
temp = gmml.Assembly()

# Set the usage statement
USAGE = """
Usage:

	This program searches Glycan structures based on the given pattern.
	
	Command:
	   python3 GlyFinderExtractNameSequenceByRegex.py oligoNameSequencePattern [output_type]

        where:
            oligoNameSequencePattern is Pattern for which
               you want to extract structure information from ontology.
               Sample Patterns:
			    *DGlcpNAcb*DGlc*
				*b1-4L*
			    DGlcpNAcb1-4DGlcpNAcb*
				*GlcpNAcb1-4DGlcpNAcb
				DGlcpNAcb*4DGlcpNAca
				*DGlcpNAcb1-4DGlcpNAcb
				DGlcpNAcb*DGlc*
				*DGlcpNAcb*GlcpNAcb
				DGlcpNAcb*GlcpNAcb
				*DManpa1-6[DManpa1-2DManpa1-3]D*

            output_type is the type of output that you want results in.
               e.g. csv, xml or json
               The default output_type is csv.
"""

# check out the command line
if len(sys.argv)<2:
    print ("""

Error:  Insufficient number of arguments.

""")
    print (USAGE)
    sys.exit(1)
	
if len(sys.argv) == 3:
	temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
	temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex(sys.argv[1])
