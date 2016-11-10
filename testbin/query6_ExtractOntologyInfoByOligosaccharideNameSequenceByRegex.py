### Sample usage from testbin directory: python query6.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the given pattern. ExtractOntologyInfoByOligosaccharideNameSequenceByRegex(pattern, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()


### Sample pattern: DGlcpNAcb1-4DGlcpNAcb
### Sample pattern: DGlcpNAcb1-4DGlc*
### Sample pattern: *b1-4L*
### Sample pattern: *GlcpNAcb1-4DGlcpNAcb
### Sample pattern: DGlcpNAcb*4DGlcpNAca
### Sample pattern: *DGlcpNAcb1-4DGlcpNAcb
### Sample pattern: *DGlcpNAcb1-4DGlc*
### Sample pattern: DGlcpNAcb*DGlc*
### Sample pattern: *DGlcpNAcb*GlcpNAcb
### Sample pattern: DGlcpNAcb*GlcpNAcb
### Sample pattern: *DGlcpNAcb*DGlc*
### Sample pattern: *DManpa1-6[DManpa1-2DManpa1-3]D*
### Change the first input argument in the function calls as you desire. ExtractOntologyInfoByOligosaccharideNameSequenceByRegex(pattern, output_type)
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb1-4DGlc*", sys.argv[1])
else:
	temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb1-4DGlc*")
