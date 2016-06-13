import sys
sys.path.insert(0, '../../')
import gmml
temp = gmml.Assembly()
temp.ExtractOntologyInfoByOligosaccharideNameSequenceByRegex(sys.argv[1], "*DManpa1-6[DManpa1-2DManpa1-3]D*")

