### Sample usage from testbin directory: python query5.py &> [YOUR-OUTPU-FILE]
### This query searches Glycan structures based on the given oligosaccharide sequence. ExtractOntologyInfoByOligosaccharideNameSequence(oligo_sequence)
import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()
temp.ExtractOntologyInfoByOligosaccharideNameSequence("DGlcpNAcb1-4DGlcpNAcb")
