### Sample usage from testbin directory: python query4.py &> [YOUR-OUTPU-FILE]
### This query searches Glycan structures based on the given chemical code. ExtractOntologyInfoByStringChemicalCode(chemical_code)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()
temp.ExtractOntologyInfoByStringChemicalCode("_4^2^3P^a^+1")
