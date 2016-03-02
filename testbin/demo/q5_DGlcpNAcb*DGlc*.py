import sys
sys.path.insert(0, '../../')
import gmml
temp = gmml.Assembly()

temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex("DGlcpNAcb*DGlc*")
