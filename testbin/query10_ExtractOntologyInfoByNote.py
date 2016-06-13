### Sample usage from testbin directory: python query10.py &> [YOUR-OUTPUT-FILE]
### This query searches PDB files that may have been assigned a note(issue) during processing them. ExtractOntologyInfoByNote(pdb_id,  note_type, note_category, output_type)

import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()


### Options for note_type: "warning", "error", "comment"
### Options for note_category: "glycosidic linkage", "anomeric", "derivative/modification", "residue name"
### Change the first 3 input arguments in the function calls as you desire. ExtractOntologyInfoByNote(pdb_id,  note_type, note_category, output_type)
if len(sys.argv) == 2:
	temp.ExtractOntologyInfoByNote("", "warning", "", sys.argv[1])
else:
	temp.ExtractOntologyInfoByNote("", "error", "")



