### Sample usage from testbin directory: python query3.py &> [YOUR-OUTPU-FILE]
### This query searches Glycan structures based on the given PDB ID. ExtractOntologyInfoByPDBID(pdb_id)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()
temp.ExtractOntologyInfoByPDBID("4A2G")
