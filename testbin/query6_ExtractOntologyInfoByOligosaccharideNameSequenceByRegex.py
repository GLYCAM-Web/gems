### Sample usage from testbin directory: python query6.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the given pattern. ExtractOntologyInfoByOligosaccharideNameSequenceByRegex(pattern)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb1-4DGlc*")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("*b1-4L*")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("*GlcpNAcb1-4DGlcpNAcb")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb*4DGlcpNAca")

temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb1-4DGlcpNAcb")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb1-4DGlc*")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("*DGlcpNAcb1-4DGlcpNAcb")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("*DGlcpNAcb1-4DGlc*")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb*DGlc*")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("*DGlcpNAcb*GlcpNAcb")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb*GlcpNAcb")
#temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("*DGlcpNAcb*DGlc*")
