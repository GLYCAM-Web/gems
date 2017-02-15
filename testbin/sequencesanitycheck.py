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
		assembly.BuildAssemblyFromCondensedSequence(sys.argv[2], sys.argv[4], sys.argv[6], True)
		pdb_file = assembly.BuildPdbFileStructureFromAssembly()
		pdb_file.Write('pdb_file.pdb')
		print('Charge: ' + str(round(assembly.GetTotalCharge(),4)))
		condensed_sequence = gmml.CondensedSequence(sys.argv[2])
		names = gmml.int_string_map()
		rotamers_glycosidic_angles_info = condensed_sequence.GetCondensedSequenceRotamersAndGlycosidicAnglesInfo(condensed_sequence.GetCondensedSequenceResidueTree())

		"""# Remove tg rotamer of OMEGA angle for 'DGalpA1-6DGlcpA' linkage if exists in selected rotamers for the specific linkage
		new_rotamers_glycosidic_angles_info = gmml.rotamer_angle_info_vector()
		for rotamers_name, rotamers_info in rotamers_glycosidic_angles_info:
			if rotamers_name == 'DGalpA1-6DGlcpA':
				new_selected_rotamers = gmml.string_vector_string_pair_vector()
				for sr_name, sr_val in rotamers_info.selected_rotamers_:
					if sr_name == 'omega':
						new_omega_selected_rotamers = gmml.string_vector()
						for val in sr_val:
							if val != 'tg':
								new_omega_selected_rotamers.push_back(val)
						new_selected_rotamers.push_back([sr_name, new_omega_selected_rotamers])
					else:
						new_selected_rotamers.push_back([sr_name, sr_val])				
				rotamers_info.selected_rotamers_ = new_selected_rotamers
			new_rotamers_glycosidic_angles_info.push_back([rotamers_name, rotamers_info])
		rotamers_glycosidic_angles_info = new_rotamers_glycosidic_angles_info

		# Add tg rotamer of OMEGA for 'DGalpA1-6DGlcpA' linkage if tg is one of the possible rotamers for the specifi linkage
		new_rotamers_glycosidic_angles_info = gmml.rotamer_angle_info_vector()
		for rotamers_name, rotamers_info in rotamers_glycosidic_angles_info:
			if rotamers_name == 'DGalpA1-6DGlcpA':
				is_possible = False
				for pr_name,pr_val in rotamers_info.possible_rotamers_:
					if pr_name == 'omega':
						for val in pr_val:
							if val == 'tg':
								is_possible = True
								break
				if is_possible:
					new_selected_rotamers = gmml.string_vector_string_pair_vector()
					for sr_name, sr_val in rotamers_info.selected_rotamers_:
						if sr_name == 'omega':
							new_omega_selected_rotamers = gmml.string_vector()
							for val in sr_val:
								if val != 'tg':
									new_omega_selected_rotamers.push_back(val)
							new_omega_selected_rotamers.push_back('tg')
							new_selected_rotamers.push_back([sr_name, new_omega_selected_rotamers])
						else:
							new_selected_rotamers.push_back([sr_name, sr_val])				
					rotamers_info.selected_rotamers_ = new_selected_rotamers
			new_rotamers_glycosidic_angles_info.push_back([rotamers_name, rotamers_info])
		rotamers_glycosidic_angles_info = new_rotamers_glycosidic_angles_info

		# Set OMEGA angle of 'DGalpA1-6DGlcpA' to a constant value = 160 if it is enabled
		new_rotamers_glycosidic_angles_info = gmml.rotamer_angle_info_vector()
		for rotamers_name, rotamers_info in rotamers_glycosidic_angles_info:
			if rotamers_name == 'DGalpA1-6DGlcpA':
				is_enabled = False
				for ga_name, ga_val in rotamers_info.enabled_glycosidic_angles_:
					if ga_name == 'omega':						
						is_enabled = True
						break
				if is_enabled:
					new_enabled_angles = gmml.glycosidic_angle_name_value_pair_vector()
					for ga_name, ga_val in rotamers_info.enabled_glycosidic_angles_:
						if ga_name == 'omega':
							new_enabled_angles.push_back([ga_name, 160])
						else:
							new_enabled_angles.push_back([ga_name, ga_val])				
					rotamers_info.enabled_glycosidic_angles_ = new_enabled_angles
			new_rotamers_glycosidic_angles_info.push_back([rotamers_name, rotamers_info])
		rotamers_glycosidic_angles_info = new_rotamers_glycosidic_angles_info"""
		
	

		print("Total number of structures with selected rotamers: " + str(condensed_sequence.CountAllPossibleSelectedRotamers(rotamers_glycosidic_angles_info) * condensed_sequence.CountAllPossible28LinkagesRotamers(rotamers_glycosidic_angles_info)))

		for rotamer_name, rotamers_info in rotamers_glycosidic_angles_info:
			print('(' + str(rotamers_info.linkage_index_) + ') ' + rotamer_name)
			p_rotamers = ""
			for pr_name, pr_val in rotamers_info.possible_rotamers_:
				for val in pr_val:
					p_rotamers += val + ", "
			s_rotamers = ""
			for sr_name, sr_val in rotamers_info.selected_rotamers_:
				for val in sr_val:
					s_rotamers += val + ", "
			e_angles = ""
			for ga_n, ga_v in rotamers_info.enabled_glycosidic_angles_:
				if ga_v != gmml.dNotSet:
					e_angles += ga_n + ": " + str(ga_v) + ", "
				else:
					e_angles += ga_n + ": _ , "
			print("possible rotamers: " + p_rotamers)
			print("default rotamers: " + s_rotamers)
			print("enabled angles: " + e_angles)
		names = gmml.int_string_map()
		structures = assembly.BuildAllRotamersFromCondensedSequence(sys.argv[2], sys.argv[4], sys.argv[6], rotamers_glycosidic_angles_info, names)
		i = 0
		for structure in structures:
			pdb_file = structure.BuildPdbFileStructureFromAssembly(-1, 0)			
			pdb_file.Write('pdb_file_' + names[i] + '.pdb')
			i += 1
		_map = condensed_sequence.CreateBaseMapAllPossibleSelectedRotamers(rotamers_glycosidic_angles_info)
		map_str = ""
		for m in _map:
			map_str += "<"
			for val in m:
				map_str = map_str + str(val) + " "
			map_str += ">"
		print(map_str)
		#condensed_sequence.CreateIndexLinkageConfigurationMap(rotamers_glycosidic_angles_info, names)
	else:
		print(sys.argv[2],' is not valid')
else:
	print('Please enter a sequence using -seq option, prep file using -prep, and parameter file using -parm as first, second and third arguments')
