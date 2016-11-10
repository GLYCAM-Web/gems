### Sample usage from testbin directory: python query8.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan structures based on the given atoms index and derivative/modification pattern. ExtractOntologyInfoByDerivativeModificationMap(ring_type, derivative_modification_map, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()

derivative_modification_map = gmml.residue_name_map()

### Options for the index: 
### '-1' for exocyclic carbon attached to the anomeric carbon of the ring
### '1' for anomeric carbon of the ring
### '2' for second carbon of the ring
### '3' for third carbon of the ring
### '4' for fourth carbon of the ring (specific to pyranoses)
### '+1' for the first exocyclic carbon attached to the last carbon of the ring
### '+2' for the second exocyclic carbon attached to the last carbon of the ring
### '+3' for the third exocyclic carbon attached to the last carbon of the ring
### Options for Pattern:
### 'xCH-N'
### 'xC-N-C=OCH3'
### 'xC-N-C=OCH2OH'
### 'xC-N-SO3'
### 'xC-N-PO3'
### 'xC-N-CH3'
### 'xC-O-C=OCH3'
### 'xC-O-C=OCH2OH'
### 'xC-O-SO3'
### 'xC-O-PO3'
### 'xC-O-CH3'
### 'xC-(O,O)'
### 'xC-(O,OH)'

### In the following line give the atom index and the pattern you want to search (derivative_modification_map['INDEX'] = 'PATTERN')
derivative_modification_map['2'] = 'xC-N-C=OCH3'


### ExtractOntologyInfoByDerivativeModificationMap(ring_type, derivative_modification_map, output_type)
### Change the first input argument in the function calls as you desire. ('F' for furanoses and 'P' for pyranoses)
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByDerivativeModificationMap('F', derivative_modification_map, sys.argv[1])
else:
	temp.ExtractOntologyInfoByDerivativeModificationMap('F', derivative_modification_map)

