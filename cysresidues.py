###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE

import gmml

temp = gmml.PdbPreprocessor()

#GIVE THE ADDRESS OF THE PDB FILE TO EXTRACT THE INFORMATION OR GIVE IT BY THE COMMAND LINE:
temp.ExtractCYSResidues("gmml/example/pdb/1RVZ_New.pdb")
#temp.ExtractCYSResidues(sys.argv[1])

disulfide_bonds = temp.GetDisulfideBonds()
for x in xrange(0, disulfide_bonds.size()):
        disulfide_bonds[x].Print()

pdbfile = gmml.PdbFile("gmml/example/pdb/1RVZ_New.pdb")

###UPDATING CYS RESIDUES###
disulfide_bonds[0].SetIsBonded(False)
print "Updated disulfide bond(s):"
disulfide_bonds[0].Print()
temp.UpdateCYSResidues(pdbfile, disulfide_bonds)

pdbfile.Write('1RVZ_New-cysresidues-update1.pdb')

