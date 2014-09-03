###IMPORTING THE GMML LIBRARY
import gmml
import sys

###BUILDING AN OBJECT OF THE PDB PREPROCESSOR AND STORING IT IN "temp" VARIABLE TO WORK WITH
temp = gmml.PdbPreprocessor()

###FIRST OPTION TO LOAD THE PDB FILE IS TO GIVE THE PATH OF THE FILE DIRECTLY IN THE CURRENT PYTHON FILE (IF YOU WANT TO USE THE SECOND OPTION COMMENT THE FIRST ONE)
#temp.ExtractAlternateResidue("gmml/example/pdb/1Z7E-Mod.pdb")

###SECOND OPTION IS TO GIVE THE PATH OF THE FILE THROUGH THE COMMAND LINE, i.e.: python alternateresidues.py gmml/example/pdb/1Z7E-Mod.pdb
temp.ExtractAlternateResidue(sys.argv[1])

###GETTING THE RESULT FOR THE ALTERNATE RESIDUES OF THE GIVEN FILE
alternate_residues_map = temp.GetAlternateResidueMap()

###IF YOU WANT TO SEE THE RESULT IN THE TERMINAL USE THE FOLLOWING FOR LOOP OTHERWISE IGNORE AND COMMENT THE LOOP
for x in alternate_residues_map:
        alternate_residues_map[x].Print()

###THIS LINE GOES WITH THE FIRST OPTION TO BUILD THE PDB FILE OBJECT (IF YOU WANT TO USE THE SECOND OPTION COMMENT IT)
#pdbfile = gmml.PdbFile("gmml/example/1Z7E-Mod.pdb")

###THIS LINE GOES WITH THE SECOND OPTION TO BUILD THE PDB FILE OBJECT
pdbfile = gmml.PdbFile(sys.argv[1])

###UPDATING ALTERNATE RESIDUES###
###GETTING THE OBJECT OF FIRST RESIDUE WITH ALTERNATE LOCATIONS (KEY OF THE alternate_residues_map IS THE COMBINATION OF "residuename_chainId_sequenceNumber_insertionCode")
selected_alt_residue = alternate_residues_map['LEU_F_657_ '].GetSelectedAlternateLocation()
###CHANGING THE ALTERNATE RESIDUE FROM A TO B
selected_alt_residue[0] = 0
selected_alt_residue[1] = 1
###APPLY THE CHANGES TO THE FIRST ALTERNATE RESIDUE OBJECT
alternate_residues_map['LEU_F_657_ '].SetSelectedAlternateLocation(selected_alt_residue)
###PRINT TO SEE THE CHANGES YOU HAVE MADE
print "The updated alternate residue locations:"
alternate_residues_map['LEU_F_657_ '].Print()

###REMOVING THE UNSELECTED ALTERNATE RESIDUES FROM THE PDB OBJECT
temp.RemoveUnselectedAlternateResidues(pdbfile, alternate_residues_map)

###THIS LINE WRITES THE CURRENT PDB OBJECT INTO A FILE WITH THE GIVEN PATH AND NAME
pdbfile.Write('1Z7E-Mod-alternateresidues.pdb')

