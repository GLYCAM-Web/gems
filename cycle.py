###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python cycle.py -amino_libs ""gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib""

import gmml
het = gmml.string_vector()
amino_libs = gmml.string_vector()

i = 1
if sys.argv[0] == '-amino_libs':  
	for i, arg in enumerate(sys.argv):
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			amino_libs.push_back(argument)

amino_libs.push_back(amino_libs);

#het.push_back("../../Downloads/DAldoHexaF/DGlcfb.pdb")
#het.push_back("../../Downloads/glycam_gg_gg_gg_gg.pdb")
#het.push_back("../../Downloads/1 (7).pdb")
het.push_back("../../Downloads/1 (7).pdb")
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
temp = gmml.Assembly(het, gmml.PDB)
empty = gmml.string_vector()
temp.BuildStructure(gmml.DISTANCE, empty, empty)

temp.ExtractSugars(amino_libs)

