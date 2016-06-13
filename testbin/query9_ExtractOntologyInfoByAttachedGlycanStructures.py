### Sample usage from testbin directory: python query9.py &> [YOUR-OUTPUT-FILE]
### This query searches two Glycan structures that are attached to each other based on the given 3D structures. ExtractOntologyInfoByAttachedGlycanStructures(structures, output_type)

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

### In the following lines the 3D structure of the first sugar is being defiend based on the orientation of the exocyclic atoms with respect to the ring
structure1 = gmml.string_vector()
### Change the following line based on the ring type (P or F)
structure1.push_back("P");
### Change the following line based on the orientation of the exocyclic oxygen/nitrogen attached to the anomeric carbon of the ring. leave "" if don't want to specify.
structure1.push_back("Up");
### Change the following line based on the orientation of the exocyclic carbon attached to the anomeric carbon of the ring. leave "" if don't want to specify.
structure1.push_back("");
### Change the following line based on the orientation of the exocyclic oxygen/nitrogen attached to the second carbon of the ring. leave "" if don't want to specify.
structure1.push_back("Down");
### Change the following line based on the orientation of the exocyclic oxygen/nitrogen attached to the third carbon of the ring. leave "" if don't want to specify.
structure1.push_back("Up");
### Change the following line based on the orientation of the exocyclic oxygen/nitrogen attached to the fourth carbon of the ring (specific to pyranoses). leave "" if don't want to specify.
structure1.push_back("Down");
### Change the following line based on the orientation of the exocyclic oxygen/nitrogen attached to the third carbon of the ring. leave "" if don't want to specify.
structure1.push_back("Up");

### In the following lines the 3D structure of the second sugar is being defiend based on the orientation of the exocyclic atoms with respect to the ring
structure2 = gmml.string_vector()
structure2.push_back("P");
structure2.push_back("Up");
structure2.push_back("");
structure2.push_back("Down");
structure2.push_back("Up");
structure2.push_back("Down");
structure2.push_back("Up");

structures = gmml.dihedral_vector()
structures.push_back(structure1)
structures.push_back(structure2)


if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByAttachedGlycanStructures(structures, argv[1])
else:
	temp.ExtractOntologyInfoByAttachedGlycanStructures(structures)


