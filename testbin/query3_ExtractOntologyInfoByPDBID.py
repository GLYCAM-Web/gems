### Sample usage from testbin directory: python query3.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the given PDB ID. ExtractOntologyInfoByPDBID(pdb_id, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()


### Change the first input argument in the function calls as you desire. ExtractOntologyInfoByPDBID(pdb_id, output_type)
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByPDBID("4A2G", sys.argv[1])
else:
	temp.ExtractOntologyInfoByPDBID("4A2G")


