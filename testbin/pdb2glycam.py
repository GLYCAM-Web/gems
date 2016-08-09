###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python cycle.py -amino_libs "../gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib" -pdb "../../../Downloads/1.pdb" -prep "../gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" &> output_file_name


import sys
sys.path.insert(0, '../')
import gmml
import time
het = gmml.string_vector()
amino_libs = gmml.string_vector()
pdb_file = ''
prep_file = ''
if len(sys.argv) < 2:
	print('Please import one pdb file using -pdb option, one prep file using -prep option  and (optionally) amino library file(s) using -amino_libs option')
elif sys.argv[1] == '-amino_libs': 
	arguments = sys.argv[2].split(',')
	for argument in arguments:
		amino_libs.push_back(argument)
	if len(sys.argv) < 4:
		print('Please import one pdb file using -pdb option and one prep file using -prep option')
	elif sys.argv[3] == '-pdb':
		pdb_file = sys.argv[4]
		if(len(sys.argv) < 6):
			print('Please import one prep file using -prep option')
		elif sys.argv[5] == '-prep':
			prep_file = sys.argv[6]
	elif sys.argv[3] == '-prep':
		prep_file = sys.argv[4]
		if(len(sys.argv) < 6):
			print('Please insert one pdb file using -pdb option')
		elif sys.argv[5] == 'pdb':
			pdb_file = sys.argv[6]
elif sys.argv[1] == '-pdb':
	pdb_file = sys.argv[2]
	if len(sys.argv) < 4:
		print('Please import one prep file using -prep option and (optionally) amino library file(s) using -amino_libs option')
	elif sys.argv[3] == '-prep':
		prep_file = sys.argv[4]
		if len(sys.argv) > 5:
			if sys.argv[3] == '-amino_libs':
				arguments = sys.argv[4].split(',')
				for argument in arguments:
					amino_libs.push_back(argument)
	elif sys.argv[3] == '-amino_libs':
		arguments = sys.argv[4].split(',')
		for argument in arguments:
			amino_libs.push_back(argument)
		if len(sys.argv) < 6:
			print('Please import one prep file using -prep option')
		elif sys.argv[5] == '-prep':
			prep_file = sys.argv[6]
elif sys.argv[1] == '-prep':
	prep_file = sys.argv[2]
	if len(sys.argv) < 4:
		print('Please import one pdb file using -pdb option and (optionally) amino library file(s) using -amino_libs option')
	elif sys.argv[3] == '-pdb':
		pdb_file = sys.argv[4]
		if len(sys.argv) > 5:
			if sys.argv[3] == '-amino_libs':
				arguments = sys.argv[4].split(',')
				for argument in arguments:
					amino_libs.push_back(argument)
	elif sys.argv[3] == '-amino_libs':
		arguments = sys.argv[4].split(',')
		for argument in arguments:
			amino_libs.push_back(argument)
		if len(sys.argv) < 6:
			print('Please import a pdb file using -pdb option')
		elif sys.argv[5] == '-pdb':
			pdb_file = sys.argv[6]
else:
	print('Please import one pdb file using -pdb option and (optionally) amino library file(s) using -amino_libs option'		)
	

if pdb_file != '':
	het.push_back(pdb_file)
	temp = gmml.Assembly(het, gmml.PDB)
	empty = gmml.string_vector()
	start = time.time()
	temp.BuildStructureByDistance(10)
	end = time.time()
	print('Time of building structure by distance:',end - start,'(sec)')
	oligos = temp.ExtractSugars(amino_libs)
	res_map = temp.ExtractResidueGlycamNamingMap(oligos)
	temp.UpdateResidueName2GlycamName(res_map, prep_file)
	pdb = temp.BuildPdbFileStructureFromAssembly()
	pdb.Write('glycam_pdb.pdb')


