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
   



# import gems/gmml stuff
sys.path.append(GemsPath)
import gmml

def getPrepFileName():
	print("Getting prepfile name.")
	try:
		prepFileName = sys.argv[5]
		return prepFileName
	except Exception as error:
		print("There was a problem getting the prepfile.")
		print("Error type: " + str(type(error)))
		print("Error details: " + str(error))
		return error

def doTheBuild(sequence, id):
	print("~~~ buildFromSequence.py's doTheBuild() was called.")
	print("sequence: " + sequence)
	print("id: " + id)



def main():
	print("~~~ buildFromSequence.py was called.")
	thisFileName = sys.argv[0]

	testVar = getPrepFileName()
	print("testVar type: " + str(type(testVar)))
	if(str(type(testVar)) != "str"):
		print("There was an issue getting the prepFile.")
		print("error: " + str(testVar))
	else:
		print("testVar: " + testVar)

	prepFileName = sys.argv[1]
	
	sequence = sys.argv[2]
	
	outOffFileName = sys.argv[3]
	
	outPdbFileName = sys.argv[4]

	#print("thisFile: " + thisFileName)
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