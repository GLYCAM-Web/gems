import sys
sys.path.insert(0, '../')
import gmml
import time

empty_vector = gmml.string_vector()
preps = gmml.string_vector()
preps.push_back(sys.argv[2])
assembly = gmml.Assembly()
assembly.BuildAssemblyFromPdbFile(sys.argv[1], empty_vector, empty_vector, empty_vector, preps, sys.argv[3])
assembly.BuildStructureByDistance(1)
output = assembly.BuildPrepFileStructureFromAssembly(sys.argv[3])
output.Write(sys.argv[4])
