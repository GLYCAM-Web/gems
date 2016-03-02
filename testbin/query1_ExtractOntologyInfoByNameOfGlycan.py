### Sample usage from testbin directory: python query1.py &> [YOUR-OUTPU-FILE]
### This query searches Glycan structures based on the given names. ExtractOntologyInfoByNameOfGlycan(stereo_name,  stereo_condensed_name, name, condensed_name)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()
temp.ExtractOntologyInfoByNameOfGlycan("", "", "", "DGlcpNAcb")
#temp.ExtractOntologyInfoByNameOfGlycan("Unknown", "", "", "")
