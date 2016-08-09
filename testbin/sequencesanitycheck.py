###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python sequencesanitycheck.py -seq "LManpa1-2[LGalpa1-3LGlcpa1-4]DGalpa1-4DGlcpa1-6DAllpa1-OH" -prep "../gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -parm "../gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j.dat"


import sys
sys.path.insert(0, '../')
import gmml
import time
if len(sys.argv) < 2:
	print('Please enter a sequence using -seq option')
elif len(sys.argv) < 8: 
	assembly = gmml.Assembly()
	prep_residues = gmml.condensedsequence_amber_prep_residue_tree()
	if assembly.CheckCondensedSequenceSanity(sys.argv[2], prep_residues):
		print(sys.argv[2],' is valid')
		assembly.BuildAssemblyFromCondensedSequence(sys.argv[2], sys.argv[4], sys.argv[6], False)
		print('Charge: ' + str(assembly.GetTotalCharge()))
		condensed_sequence = gmml.CondensedSequence(sys.argv[2])
		rotomers_glycosidic_angles_info = condensed_sequence.GetCondensedSequenceRotomersAndGlycosidicAnglesInfo(condensed_sequence.GetCondensedSequenceResidueTree())
		for rotomer_name, rotomers_info in rotomers_glycosidic_angles_info:
			print(rotamer_name)
			p_rotomers = ""
			for pr in rotomers_info.possible_rotomers_:
				p_rotomers += pr + ", "
			d_rotomers = ""
			for dr in rotomers_info.default_seleted_rotomers_:
				d_rotomers += dr + ", "
			e_angles = ""
			for ga in rotomers_info.enabled_glycosidic_angles_:
				e_angles += ga + ", "
			print("possible rotamers: " + p_rotomers)
			print("default rotamers: " + d_rotomers)
			print("enabled angles: " + e_angles)
	else:
		print(sys.argv[2],' is not valid')
else:
	print('Please enter a sequence using -seq option, prep file using -prep, and parameter file using -parm as first, second and third arguments')
