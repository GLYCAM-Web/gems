### Sample usage from testbin directory: python query7.py &> [YOUR-OUTPU-FILE]
### This query searches Glycan structures based on the given side atom orientations. 
### ExtractOntologyInfoByGlycanStructure(ring_type, anomeric_orientation, anomeric_side_carbon_orientation, index_two_orientation, index_three_orientation, index_four_orientation,  last_c_orientation)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()
temp.ExtractOntologyInfoByGlycanStructure("P", "Up", "", "Up","Up", "Down", "Down")
