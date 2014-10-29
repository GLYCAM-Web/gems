###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python gapsinaminoacidchains.py -libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib" -pdb "gmml/example/pdb/1Z7E.pdb"

import gmml
import sys

temp = gmml.PdbPreprocessor()
libs = gmml.string_vector()

for i, arg in enumerate(sys.argv):	
    if arg == '-libs':                       
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			libs.push_back(argument)
    elif arg == '-pdb':
		pdb = sys.argv[i+1]

pdbfile = gmml.PdbFile(pdb)

temp.ExtractGapsInAminoAcidChains(pdbfile)

missing_residues = temp.GetMissingResidues()
for x in xrange(0, missing_residues.size()):
        missing_residues[x].Print()


###UPDATING GAPS IN AMINO ACID CHAINS###
#MODIFYING n_termination and c_termination ATTRIBUTES OF THE CHAIN TERMINATIONS VECTOR:
#POSSIBLE n_termination OPTIONS: gmml.COCH3, gmml.NH3
#POSSIBLE c_termination OPTIONS: gmml.NH2, gmml.NHCH3, gmml.CO2
missing_residues[0].SetSelectedNTermination(gmml.NH3)
missing_residues[0].SetSelectedCTermination(gmml.NH2)

temp.UpdateGapsInAminoAcidChains(pdbfile, libs, missing_residues)

pdbfile.Write('gapsinaminoacidchains-update.pdb')

