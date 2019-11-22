#!/usr/bin/env python3
import sys
import os
import gmml


def getPrepFileName():
#    print("Getting prepfile name.")
    try:
        prepFileName = sys.argv[1]
        return prepFileName
    except Exception as error:
#        print("There was a problem getting the prepfile.")
#        print("Error type: " + str(type(error)))
#        print("Error details: " + str(error))
        return error

#buildThis(theSequence,  prepFile, offFile, pdbFile)
# TODO: fix this. It breaks everything.
def buildThis(sequence, prepFile, offFile, pdbFile):
#    print("~~~ buildFromSequence.py's doTheBuild() was called.")
#    print("sequence: " + sequence)
#    print("prepFile: " + prepFile)
#    print("offFile: " + offFile)
#    print("pdbFile: " + pdbFile)

    prep = gmml.PrepFile(prepFile)
    assembly = gmml.Assembly()
    assembly.SetName("CONDENSEDSEQUENCE")
    assembly.BuildAssemblyFromCondensedSequence(sequence, prep)
    assembly.CreateOffFileFromAssembly(offFile, 0)
    content = assembly.BuildPdbFileStructureFromAssembly()

    content.Write(pdbFile)



def logHello():
    print("Hello")

def main():
#    print("~~~ buildFromSequence.py was called.")
    thisFileName = sys.argv[0]

    prepFileName = sys.argv[1]

    sequence = sys.argv[2]

    outOffFileName = sys.argv[3]

    outPdbFileName = sys.argv[4]

    #print("thisFile: " + thisFileName)
#    print("prepFile: " + prepFileName)
#    print("sequence: " + sequence)
#    print("outOff: " + outOffFileName)
#    print("outPdb: " + outPdbFileName)

    prep = gmml.PrepFile(prepFileName)
    assembly = gmml.Assembly()
    assembly.SetName("CONDENSEDSEQUENCE")
    assembly.BuildAssemblyFromCondensedSequence(sequence, prep)
    assembly.CreateOffFileFromAssembly(outOffFileName, 0)
    content = assembly.BuildPdbFileStructureFromAssembly()

    content.Write(outPdbFileName)


if __name__ == "__main__":
    main()
