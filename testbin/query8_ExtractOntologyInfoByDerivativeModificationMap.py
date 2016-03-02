### Sample usage from testbin directory: python query8.py &> [YOUR-OUTPU-FILE]
### This query searches Glycan structures based on the given atom_index-dervative/modification map. ExtractOntologyInfoByDerivativeModificationMap(ring_type, derivative_modification_map)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()

derivative_modification_map = gmml.residue_name_map()
derivative_modification_map['2'] = 'xC-N-C=OCH3'
temp.ExtractOntologyInfoByDerivativeModificationMap('P', derivative_modification_map)
