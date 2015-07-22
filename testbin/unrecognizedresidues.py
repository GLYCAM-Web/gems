###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python unrecognizedresidues.py -amino_libs "gmml/dat/lib/GLYCAM_amino_06h.lib","gmml/dat/lib/GLYCAM_aminoct_06h.lib","gmml/dat/lib/GLYCAM_aminont_06h.lib" -prep "gmml/dat/prep/Glycam_06.prep" -pdb "gmml/example/pdb/1Z7E.pdb"

#If you need to add other libraries for glycam and other residues there are -glycam_libs and -other_libs options available for the command.

import gmml
import sys
temp = gmml.PdbPreprocessor()
amino_libs = gmml.string_vector()
glycam_libs = gmml.string_vector()
other_libs = gmml.string_vector()
prep = gmml.string_vector()

if sys.argv[1] == '--help':  
	print 'Available options:'
	print '-amino_libs : amino acid library file(s) (e.g. gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib)'
	print '-glycam_libs: glycam library file(s)'
	print '-other_libs : other kinds of library files'
	print '-prep       : prep file(s) (e.g. gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep)'
	print '-pdb        : pdb file (e.g. gmml/example/pdb/1RVZ_New.pdb)'
	print '-cnf        : configuration file as an argument. sample file format:'
	print 'amino_libs'
	print 'gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib'
	print 'gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib'
	print 'glycam_libs'
	print 'other_libs'
	print 'prep'
	print 'gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep'
	print 'pdb'
	print 'gmml/example/pdb/1RVZ_New.pdb'
	sys.exit()
elif sys.argv[1] == '-cnf':      
	with open(sys.argv[2], 'r') as my_file:
	    conf_file = my_file.readlines()
	for i in range(0, len(conf_file)):
		conf_file[i] = conf_file[i].strip()
	i = 0
	if conf_file[i] == 'amino_libs':
		i = i+1
		while conf_file[i] != 'glycam_libs':
			amino_libs.push_back(conf_file[i])
			i = i+1	
		i = i+1
		while conf_file[i] != 'other_libs':
			glycam_libs.push_back(conf_file[i])
			i = i+1	
		i = i+1
		while conf_file[i] != 'prep':
			other_libs.push_back(conf_file[i])
			i = i+1	
		i = i+1
		while conf_file[i] != 'pdb':
			prep.push_back(conf_file[i])
			i = i+1	
		i = i+1
		pdb = conf_file[i]
	else:
		print 'invalid configuration file format'
else:
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
temp.ExtractUnrecognizedResidues(pdbfile, amino_libs, glycam_libs, other_libs, prep)	


###FOR GIVING THE FILES MANUALLY AND THROUGH THE COMMAND LINE USE THE FOLOWIG SECTION
#amino_libs.push_back("gmml/dat/lib/GLYCAM_amino_06h.lib")
#amino_libs.push_back("gmml/dat/lib/GLYCAM_aminoct_06h.lib")
#amino_libs.push_back("gmml/dat/lib/GLYCAM_aminont_06h.lib")
#prep.push_back("gmml/dat/prep/Glycam_06.prep")
#temp.ExtractUnrecognizedResidues("gmml/example/pdb/1Z7E.pdb", amino_libs, glycam_libs, other_libs, prep)


unrecognized_residues = temp.GetUnrecognizedResidues()
for x in xrange(0, unrecognized_residues.size()):
        unrecognized_residues[x].Print()


temp.RemoveUnrecognizedResidues(pdbfile, unrecognized_residues)
pdbfile.Write('unrecognizedresidue-update.pdb')

