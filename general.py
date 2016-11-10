#!/usr/bin/env python
###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE

import gmml
import sys
temp = gmml.PdbPreprocessor()
#libs = gmml.string_vector()
#prep = gmml.string_vector()
amino_libs = gmml.string_vector()
glycam_libs = gmml.string_vector()
other_libs = gmml.string_vector()
prep = gmml.string_vector()

amino_libs.push_back("/programs/gems/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib")
amino_libs.push_back("/programs/gems/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
amino_libs.push_back("/programs/gems/gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/aminont12.lib")
prep.push_back("/programs/gems/gmml/dat/CurrentParams/leaprc_GLYCAM_06j-1_2014-03-14/GLYCAM_06j-1.prep")
#libs.push_back("/programs/temp/gems/gmml/dat/lib/GLYCAM_amino_06h.lib")
#libs.push_back("/programs/temp/gems/gmml/dat/lib/GLYCAM_aminoct_06h.lib")
#libs.push_back("/programs/temp/gems/gmml/dat/lib/GLYCAM_aminont_06h.lib")
#libs.push_back("/programs/temp/gems/gmml/dat/lib/tip3pbox.off")

for i, arg in enumerate(sys.argv):	
	if arg == '-libs':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			libs.push_back(argument)
	elif arg == '-prep':
		arguments = sys.argv[i+1].split(',')
		for argument in arguments:
			prep.push_back(argument)
	elif arg == '-pdb':
    		pdb = sys.argv[i+1]

#temp.Preprocess(pdb, libs, prep)

#pdbfile = gmml.PdbFile(pdb)

#GIVE THE ADDRESS OF THE PDB FILE TO EXTRACT THE INFORMATION OR GIVE IT BY THE COMMAND LINE:

#print "begin\n"

#pdb = "/programs/temp/gems/gmml/example/pdb/1RVZ_New.pdb"
fileO = open(pdb, 'r')
fileN = open(pdb+"_withoutOXT", 'w')
for line in fileO:
    if line.find("OXT")!= -1 and line.find("ATOM")!= -1:
        print(line)
    else:
        fileN.write(line)

fileO.close()
fileN.close()
pdb = pdb + "_withoutOXT"

pdbfile = gmml.PdbFile(pdb)



temp.ExtractCYSResidues(pdbfile)#CYS   done



disulfide_bonds = temp.GetDisulfideBonds()
for x in range(0, disulfide_bonds.size()):
        disulfide_bonds[x].Print()

print("========CYS DONE========")

temp.ExtractHISResidues(pdbfile)#HIS  done

histidine_mappings = temp.GetHistidineMappings()
for x in range(0, histidine_mappings.size()):
        #print "HIS ",
        histidine_mappings[x].Print()
print("========HIS DONE========")

#temp.ExtractUnknownHeavyAtoms(pdb,libs,prep)#Heavy
temp.ExtractUnknownHeavyAtoms(pdbfile, amino_libs, glycam_libs, other_libs, prep);

unrecognized_heavy_atoms = temp.GetUnrecognizedHeavyAtoms()
for x in range(0, unrecognized_heavy_atoms.size()):
        #print "HEAVY ",
        unrecognized_heavy_atoms[x].Print()
print("=======HEAVY DONE=========")
#-pdb "gmml/example/pdb/1Z7E-Mod.pdb"

#temp.ExtractRemovedHydrogens(pdb,libs,prep)# remove  
temp.ExtractRemovedHydrogens(pdbfile, amino_libs, glycam_libs, other_libs, prep);

replaced_hydrogens = temp.GetReplacedHydrogens()
for x in range(0, replaced_hydrogens.size()):
        #print "REMOVE_HYD ",
        replaced_hydrogens[x].Print()
print("=======REMOVEHYDROGENS DONE=========")

temp.ExtractResidueInfo(pdbfile, amino_libs, glycam_libs, other_libs,prep);
#print "",
print("CHARGE ",temp.CalculateModelCharge(pdbfile, amino_libs, glycam_libs, other_libs,prep))

print("=======CALCULATEMODELCHARGE DONE=========")

#temp.ExtractUnrecognizedResidues(pdbfile,libs,prep)#Unrec  done?
temp.ExtractUnrecognizedResidues(pdbfile, amino_libs, glycam_libs, other_libs, prep);
unrecognized_residues = temp.GetUnrecognizedResidues()
print("sizeeeee",unrecognized_residues.size())
print(" ")
#print unrecognized_residues.size.size()
for x in range(0, unrecognized_residues.size()):
        print("UNREC_RES ")
        unrecognized_residues[x].Print()
print("=======UNRECRESIDUE DONE=========")

temp.ExtractAminoAcidChains(pdbfile)#chain extra   
chain_terminations = temp.GetChainTerminations()
for x in range(0, chain_terminations.size()):
       # print "CHAIN_TER ",
        chain_terminations[x].Print()
#print "========CHAIN TER DONE========"


temp.ExtractGapsInAminoAcidChains(pdbfile,amino_libs)#Gap missing  done
missing_residues = temp.GetMissingResidues()
#print "",
for x in range(0, missing_residues.size()):
        #print "MISSING_RES ",
        missing_residues[x].Print()
#print "========GAP/MISSING RESIDUE DONE========"



temp.ExtractAlternateResidue(pdb)#alter
alternate_residues_map = temp.GetAlternateResidueMap()
#print "",
for x in alternate_residues_map:
        #print "ALTER_RES ",
        alternate_residues_map[x].Print()

#print "========ALTER RESIDUE DONE========"


temp.Preprocess(pdbfile, amino_libs, glycam_libs, other_libs, prep)
temp.ApplyPreprocessingWithTheGivenModelNumber(pdbfile, amino_libs, glycam_libs, prep)



seq_map = pdbfile.GetSequenceNumberMapping()
#print "NUM_OF_MAP_RES", seq_map.size()
for x in seq_map:
        print("MAPPING",x, seq_map[x])
#print "=========RES MAP DONE============"

#print "done\n"


#pdbfile = gmml.PdbFile(pdb)

###IN ORDER TO UPDATE EACH PARTS OF THE PDB FILE YOU CAN USE THE SAME CODE FROM ANY OF THE SAMPLE FILES, i.e. cysresidues.py
###UPDATING CYS RESIDUES###
#disulfide_bonds = temp.GetDisulfideBonds()
#disulfide_bonds[0].SetIsBonded(False)

###THIS FUNCTIONS WILL APPLY ALL THE UPDATED INFORMATION
#temp.ApplyPreprocessing(pdbfile, libs)
#pdbfile.Write('updated_pdb.txt')
#pdbfile = gmml.PdbFile("/programs/temp/gems/gmml/example/pdb/1RVZ_New.pdb")

###UPDATING CYS RESIDUES###
#disulfide_bonds[0].SetIsBonded(False)
#print "Updated disulfide bond(s):"
#disulfide_bonds[0].Print()
#temp.UpdateCYSResidues(pdbfile, disulfide_bonds)

#pdbfile.Write('1RVZ_New-cysresidues-update1.pdb')


