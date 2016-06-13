### Sample usage from testbin directory: python query2.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the different given parts of the name. ExtractOntologyInfoByNamePartsOfGlycan(isomer, ring_type, configuration, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()


### isomer can be D or L
### ring_type can be p or f
### configuration can be a, b or x
### Change the first 3 input arguments in function calls as you desire. ExtractOntologyInfoByNamePartsOfGlycan(isomer, ring_type, configuration, output_type)
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByNamePartsOfGlycan("L",  "F", "alpha", sys.argv[1])
else:
	temp.ExtractOntologyInfoByNamePartsOfGlycan("L",  "F", "alpha")

