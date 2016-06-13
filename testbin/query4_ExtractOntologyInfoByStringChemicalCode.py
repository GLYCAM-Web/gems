### Sample usage from testbin directory: python query4.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the given chemical code. ExtractOntologyInfoByStringChemicalCode(chemical_code, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()


### chemical_code is the linear version of the Glycode. more information on Glycode: http://glycam.org/docs/gmml/2016/03/31/glycode-internal-monosaccharide-representation/
### Change the first input argument in the function calls as you desire. ExtractOntologyInfoByStringChemicalCode(chemical_code, output_type)
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByStringChemicalCode("_4^2^3P^a^+1", sys.argv[1])
else:
	temp.ExtractOntologyInfoByStringChemicalCode("_4^2^3P^a^+1")

