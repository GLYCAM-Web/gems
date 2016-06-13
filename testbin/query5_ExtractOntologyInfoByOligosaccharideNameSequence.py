### Sample usage from testbin directory: python query5.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the given oligosaccharide sequence. ExtractOntologyInfoByOligosaccharideNameSequence(oligo_sequence, output_type)
import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()


### Change the first input argument in the function call as you desire. ExtractOntologyInfoByOligosaccharideNameSequence(oligo_sequence, output_type)
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByOligosaccharideNameSequence("DGlcpNAcb1-4DGlcpNAcb", sys.argv[1])
else:
	temp.ExtractOntologyInfoByOligosaccharideNameSequence("DGlcpNAcb1-4DGlcpNAcb")


