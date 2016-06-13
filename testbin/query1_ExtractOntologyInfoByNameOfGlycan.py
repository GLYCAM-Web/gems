### Sample usage from testbin directory: python query1.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the given names. ExtractOntologyInfoByNameOfGlycan(stereo_name, stereo_condensed_name, name, condensed_name, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()



### Sample stereo_name: b-D-glucopyranose
### Sample stereo_condensed_name: DGlcpb
### Sample name: N-acetyl-b-D-glucopyranose
### Sample condensed_name: DGlcpNAcb
### The naming convention should conform to samples.
### Change the first 4 input arguments in the function calls as you desire. ExtractOntologyInfoByNameOfGlycan(stereo_name, stereo_condensed_name, name, condensed_name, output_type)

if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByNameOfGlycan("", "", "", "DGlcpNAcb", sys.argv[1])
else:
	temp.ExtractOntologyInfoByNameOfGlycan("", "", "", "DGlcpNAcb")
