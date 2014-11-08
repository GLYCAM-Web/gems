###SAMPLE COMMAND 
# python residueinfo.py -amino_libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -pdb "gmml/example/pdb/1NXC.pdb"

#If you need to add other libraries for glycam and other residues there are -glycam_libs and -other_libs options available for the command.

###IMPORTING THE GMML LIBRARY

import gmml
import sys


temp = gmml.PdbPreprocessor()
amino_libs = gmml.string_vector()
glycam_libs = gmml.string_vector()
other_libs = gmml.string_vector()
prep = gmml.string_vector()

for i, arg in enumerate(sys.argv):	
    if arg == '-amino_libs':                       
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			amino_libs.push_back(argument)
    elif arg == '-glycam_libs':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			glycam_libs.push_back(argument)
    elif arg == '-other_libs':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			other_libs.push_back(argument)
    elif arg == '-prep':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			prep.push_back(argument)
	elif arg == '-pdb':
		pdb = sys.argv[i+1]

pdbfile = gmml.PdbFile(pdb)

temp.ExtractResidueInfo(pdbfile, amino_libs, glycam_libs, other_libs)


###FOR GIVING THE FILES MANUALLY AND THROUGH THE COMMAND LINE USE THE FOLOWIG SECTION
#amino_libs.push_back("gmml/dat/lib/GLYCAM_amino_06h.lib")
#amino_libs.push_back("gmml/dat/lib/GLYCAM_aminoct_06h.lib")
#amino_libs.push_back("gmml/dat/lib/GLYCAM_aminont_06h.lib")
#temp.ExtractRemovedHydrogens("gmml/example/pdb/1Z7E-Mod.pdb, amino_libs, glycam_libs, other_libs)


residue_info = temp.GetResidueInfoMap()
for x in residue_info:
	residue_info[x].Print()

print 'Model charge is: ' ,temp.CalculateModelCharge(pdbfile, libamino_libs, glycam_libs, other_libs)

pdbfile.Write('residueinfo-update.pdb')

