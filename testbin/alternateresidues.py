###SAMPLE COMMAND 
# python alternateresidues.py gmml/example/pdb/1Z7E-Mod.pdb

###IMPORTING THE GMML LIBRARY
import sys
sys.path.insert(0, '../')
import gmml

###BUILDING AN OBJECT OF THE PDB PREPROCESSOR AND STORING IT IN "temp" VARIABLE TO WORK WITH
temp = gmml.PdbPreprocessor()

###FIRST OPTION TO BUILD THE PDB FILE OBJECT: GIVE YOUR PDB FILE PATH IN THE FOLLOWING LINE. (IF YOU WANT TO USE THE SECOND OPTION COMMENT THE FOLLOWING LINE)
#pdbfile = gmml.PdbFile("gmml/example/1Z7E-Mod.pdb")

###SECOND OPTION TO BUILD THE PDB FILE OBJECT. (IF YOU WANT TO USE THE FIRST OPTION COMMENT THE FOLLOWING LINE)
pdbfile = gmml.PdbFile(sys.argv[1])

###EXTRACTING INFORMATION
temp.ExtractAlternateResidue(pdbfile)

###GETTING THE RESULT FOR THE ALTERNATE RESIDUES OF THE GIVEN FILE
alternate_residues_map = temp.GetAlternateResidueMap()

###IF YOU WANT TO SEE THE RESULT IN THE TERMINAL USE THE FOLLOWING FOR LOOP OTHERWISE IGNORE AND COMMENT THE LOOP
print(alternate_residues_map)
for x in alternate_residues_map:
	alternate_residues_map[x].Print()

###UPDATING ALTERNATE RESIDUES###
###GETTING THE OBJECT OF FIRST RESIDUE WITH ALTERNATE LOCATIONS (KEY OF THE alternate_residues_map IS THE COMBINATION OF "residuename_chainId_sequenceNumber_insertionCode")
selected_alt_residue = alternate_residues_map['LEU_F_657_?'].GetSelectedAlternateLocation()
###CHANGING THE ALTERNATE RESIDUE FROM A TO B
selected_alt_residue[0] = 0
selected_alt_residue[1] = 1

###APPLY THE CHANGES TO THE FIRST ALTERNATE RESIDUE OBJECT
alternate_residues_map['LEU_F_657_?'].SetSelectedAlternateLocation(selected_alt_residue)
###PRINT TO SEE THE CHANGES YOU HAVE MADE
print("The updated alternate residue locations:")
alternate_residues_map['LEU_F_657_?'].Print()

###REMOVING THE UNSELECTED ALTERNATE RESIDUES FROM THE PDB OBJECT
temp.RemoveUnselectedAlternateResidues(pdbfile, alternate_residues_map)

###THIS LINE WRITES THE CURRENT PDB OBJECT INTO A FILE WITH THE GIVEN PATH AND NAME
pdbfile.Write('alternateresidues.pdb')

