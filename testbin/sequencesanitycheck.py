###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python sequencesanitycheck.py -seq "LManpa1-2[LGalpa1-3LGlcpa1-4]DGalpa1-4DGlcpa1-6DAllpa1-OH"


import sys
sys.path.insert(0, '../')
import gmml
import time
if len(sys.argv) < 2:
	print('Please enter a sequence using -seq option')
elif sys.argv[1] == '-seq': 
	assembly = gmml.Assembly()
	prep_residues = gmml.condensedsequence_amber_prep_residue_tree()
	if assembly.CheckCondensedSequenceSanity(sys.argv[2], prep_residues):
		print(sys.argv[2],' is valid')
	else:
		print(sys.argv[2],' is not valid')
else:
	print('Please enter a sequence using -seq option')
