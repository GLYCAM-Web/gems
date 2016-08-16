###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python sequencesanitycheck.py -seq "LManpa1-2[LGalpa1-3LGlcpa1-4]DGalpa1-4DGlcpa1-6DAllpa1-OH" -prep "../gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -parm "../gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j.dat"


import sys
sys.path.insert(0, '../')
import gmml
import time
if len(sys.argv) < 2:
	print 'Please enter a sequence using -seq option'
elif len(sys.argv) < 8: 
	assembly = gmml.Assembly()
	prep_residues = gmml.condensedsequence_amber_prep_residue_tree()
	if assembly.CheckCondensedSequenceSanity(sys.argv[2], prep_residues):
		print sys.argv[2],' is valid'
		assembly.BuildAssemblyFromCondensedSequence(sys.argv[2], sys.argv[4], sys.argv[6], True)
		print 'Charge: ' + str(assembly.GetTotalCharge())
		condensed_sequence = gmml.CondensedSequence(sys.argv[2])
		rotamers_glycosidic_angles_info = condensed_sequence.GetCondensedSequenceRotamersAndGlycosidicAnglesInfo(condensed_sequence.GetCondensedSequenceResidueTree())
		for rotomer_name, rotamers_info in rotamers_glycosidic_angles_info:
			print '(' + str(rotamers_info.linkage_index_) + ') ' + rotomer_name
			p_rotamers = ""
			for pr in rotamers_info.possible_rotamers_:
				p_rotamers += pr + ", "
			d_rotamers = ""
			for dr in rotamers_info.default_seleted_rotamers_:
				d_rotamers += dr + ", "
			e_angles = ""
			for ga in rotamers_info.enabled_glycosidic_angles_:
				e_angles += ga + ", "
			print "possible rotamers: " + p_rotamers
			print "default rotamers: " + d_rotamers
			print "enabled angles: " + e_angles
		pdb_file = assembly.BuildPdbFileStructureFromAssembly()
		pdb_file.Write('pdb_file.pdb')
	else:
		print sys.argv[2],' is not valid'
else:
	print 'Please enter a sequence using -seq option, prep file using -prep, and parameter file using -parm as first, second and third arguments'
