
###SAMPLE COMMAND 
# python residueinfo.py -libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -pdb "gmml/example/pdb/1NXC.pdb"
###IMPORTING THE GMML LIBRARY

import gmml
import sys


temp = gmml.PdbPreprocessor()
libs = gmml.string_vector()
prep = gmml.string_vector()

for i, arg in enumerate(sys.argv):	
	if arg == '-libs':                       
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			libs.push_back(argument)
	elif arg == '-pdb':
		pdb = sys.argv[i+1]

pdbfile = gmml.PdbFile(pdb)

temp.ExtractResidueInfo(pdbfile, libs)


###FOR GIVING THE FILES MANUALLY AND THROUGH THE COMMAND LINE USE THE FOLOWIG SECTION
#libs.push_back("gmml/dat/lib/GLYCAM_amino_06h.lib")
#libs.push_back("gmml/dat/lib/GLYCAM_aminoct_06h.lib")
#libs.push_back("gmml/dat/lib/GLYCAM_aminont_06h.lib")
#temp.ExtractRemovedHydrogens("gmml/example/pdb/1Z7E-Mod.pdb)


residue_info = temp.GetResidueInfoMap()
for x in residue_info:
	residue_info[x].Print()

print 'Model charge is: ' ,temp.CalculateModelCharge(pdbfile, libs)

pdbfile.Write('residueinfo-update.pdb')

