### Sample usage from testbin directory: python query7.py &> [YOUR-OUTPUT-FILE]
### This query searches Glycan 3D structures based on the given exocycclic atoms orientations.
### ExtractOntologyInfoByGlycanStructure(ring_type, anomeric_orientation, anomeric_side_carbon_orientation, index_two_orientation, index_three_orientation, index_four_orientation,  last_c_orientation, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()

### ring_type can be "P" or "F"
### orientations can be "Up" or "Down" which shows the position of the exocyclic atoms with respect to the ring
### anomeric_orientation: orientation of the exocyclic oxygen/nitrogen attached to the anomeric carbon of the ring
### anomeric_side_carbon_orientation: orientation of the exocyclic carbon attached to the anomeric carbon of the ring
### index_two_orientation: orientation of the exocyclic oxygen/nitrogen attached to the second carbon of the ring
### index_three_orientation: orientation of the exocyclic oxygen/nitrogen attached to the third carbon of the ring
### index_four_orientation: orientation of the exocyclic oxygen/nitrogen attached to the fourth carbon of the ring (specific to pyranoses)
### last_c_orientation: orientation of the exocyclic oxygen/nitrogen attached to the last carbon of the ring
### ExtractOntologyInfoByGlycanStructure(ring_type, anomeric_orientation, anomeric_side_carbon_orientation, index_two_orientation, index_three_orientation, index_four_orientation,  last_c_orientation, output_type)
### Change the first 7 input arguments in the function calls  as you desire.
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByGlycanStructure("P", "Up", "", "Up","Up", "Down", "Down", sys.argv[1])
else:
	temp.ExtractOntologyInfoByGlycanStructure("P", "Up", "", "Up","Up", "Down", "Down")

