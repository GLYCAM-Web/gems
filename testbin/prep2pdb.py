import sys
sys.path.insert(0, '../')
import gmml
import time

assembly = gmml.Assembly()
assembly.BuildAssemblyFromPrepFile(sys.argv[1], sys.argv[2])
assembly.SetSourceFile(sys.argv[1])
assembly.BuildStructureByPrepFileInformation()
output = assembly.BuildPdbFileStructureFromAssembly()
output.Write('pdb_output.pdb')


