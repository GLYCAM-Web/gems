### Sample usage from testbin directory: python query2.py &> [YOUR-OUTPU-FILE]
### This query searches Glycan structures based on the different given parts of the name. ExtractOntologyInfoByNamePartsOfGlycan(string isomer, string ring_type, string configuration)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()
temp.ExtractOntologyInfoByNamePartsOfGlycan("L",  "F", "alpha")
