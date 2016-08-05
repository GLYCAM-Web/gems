###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python sequencesanitycheck.py -seq "LManpa1-2[LGalpa1-3LGlcpa1-4]DGalpa1-4DGlcpa1-6DAllpa1-OH" -prep "../gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -parm "../gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j.dat"


import sys
sys.path.insert(0, '../')
import gmml
import time
if len(sys.argv) < 2:
	print 'Please enter a sequence using -seq option'
elif sys.argv[1] == '-seq': 
	assembly = gmml.Assembly()
	prep_residues = gmml.condensedsequence_amber_prep_residue_tree()
	if assembly.CheckCondensedSequenceSanity(sys.argv[2], prep_residues):
		print sys.argv[2],' is valid'
		assembly.BuildAssemblyFromCondensedSequence(sys.argv[2], sys.argv[4], sys.argv[6], True)
		pdb_file = assembly.BuildPdbFileStructureFromAssembly()
		pdb_file.Write('pdb_file.pdb') 
	else:
		print sys.argv[2],' is not valid'
else:
	print 'Please enter a sequence using -seq option'
