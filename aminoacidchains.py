###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python aminoacidchains.py -amino_libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib","gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminoct12.lib"-prep "gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep" -pdb "gmml/example/pdb/1Z7E.pdb"

#If you need to add other libraries for glycam there is -glycam_libs option available for the command.

import gmml
import sys

temp = gmml.PdbPreprocessor()
amino_libs = gmml.string_vector()
glycam_libs = gmml.string_vector()
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
    elif arg == '-prep':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			prep.push_back(argument)
    elif arg == '-pdb':
		pdb = sys.argv[i+1]

pdbfile = gmml.PdbFile(pdb)

temp.ExtractAminoAcidChains(pdbfile)

chain_terminations = temp.GetChainTerminations()

for x in xrange(0, chain_terminations.size()):
        chain_terminations[x].Print()


###UPDATING AMINO ACID CHAINS###
chain_terminations[0].SetSelectedNTermination(gmml.NH3)
chain_terminations[0].SetSelectedCTermination(gmml.NHCH3)
print "The Updated chain terminations:"
for x in xrange(0, chain_terminations.size()):
        chain_terminations[x].Print()

temp.UpdateAminoAcidChains(pdbfile, amino_libs, glycam_libs, prep, chain_terminations)

pdbfile.Write('aminoacidchain-update.pdb')
