###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python cycle.py -amino_libs "../gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib" -pdb "../../../Downloads/1.pdb" &> output_file_name


import sys
sys.path.insert(0, '../')
import gmml
import time
het = gmml.string_vector()
amino_libs = gmml.string_vector()
pdb_file = ''
if len(sys.argv) < 2:
	print 'Please import one pdb file using -pdb option and (optionally) amino library file(s) using -amino_libs option'
elif sys.argv[1] == '-amino_libs': 
	arguments = sys.argv[2].split(',')
	for argument in arguments:
		amino_libs.push_back(argument)
	if len(sys.argv) < 4:
		print 'Please import one pdb file using -pdb option'
	elif sys.argv[3] == '-pdb':
		pdb_file = sys.argv[4]
elif sys.argv[1] == '-pdb':
	pdb_file = sys.argv[2]
	if len(sys.argv) > 3:
		if sys.argv[3] == '-amino_libs':
			arguments = sys.argv[4].split(',')
			for argument in arguments:
				amino_libs.push_back(argument)
	
	

#het.push_back("../../Downloads/DAldoHexaF/DGlcfb.pdb")
#het.push_back("../../Downloads/glycam_gg_gg_gg_gg.pdb")
#het.push_back("../../Downloads/1 (7).pdb")
#het.push_back("../../Downloads/1 (7).pdb")
#het.push_back("../../Documents/PDB/4A2G.pdb")
#het.push_back("../../Documents/PDB/1G1Y.pdb")
#het.push_back("../../Documents/PDB/1RVZ.pdb")
#het.push_back("../../Documents/PDB/3C43.pdb")
#het.push_back("../../Documents/PDB/6CPP.pdb")
#het.push_back("../../Documents/PDB/1DMT.pdb")
#het.push_back("../../Documents/PDB/1G45.pdb")
#het.push_back("../../Documents/PDB/4HJL.pdb")
#het.push_back("../../Documents/PDB/4OBR.pdb")
#het.push_back("../../Documents/PDB/1KC3.pdb")
#het.push_back("../../Documents/PDB/4A2G_test.pdb")    	#C-N-CO-C with anomeric checked!
#het.push_back("../../Documents/PDB/4A2G_test-1.pdb")	#C-N-CO-C without anomeric checked!
#het.push_back("../../Documents/PDB/4A2G_test-2.pdb")	#C-N-CO-CO with anomeric checked!
#het.push_back("../../Documents/PDB/4A2G_test-3.pdb")	#CH-N , C-(O,O) without anomeric checked!
#het.push_back("../../Documents/PDB/4A2G_test-4.pdb")	#C-N-C with anomeric checked!
#het.push_back("../../Documents/PDB/4A2G_test-5.pdb")	#C-N-C with anomeric checked!

if pdb_file != '':
	het.push_back(pdb_file)
	temp = gmml.Assembly(het, gmml.PDB)
	empty = gmml.string_vector()
	start = time.time()
	#temp.BuildStructure(gmml.DISTANCE, empty, empty)
	temp.BuildStructureByDistance(10)
	end = time.time()
	print end - start
	oligos = temp.ExtractSugars(amino_libs)
	res_map = temp.ExtractResidueGlycamNamingMap(oligos)
	temp.UpdateResidueName2GlycamName(res_map)
	pdb = temp.BuildPdbFileStructureFromAssembly()
	pdb.Write('glycam_pdb.pdb')
	#temp.Print()


