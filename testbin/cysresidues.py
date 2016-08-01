###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE

sys.path.insert(0, '../')
import gmml

temp = gmml.PdbPreprocessor()

pdbfile = gmml.PdbFile("gmml/example/pdb/1RVZ_New.pdb")

#GIVE THE ADDRESS OF THE PDB FILE TO EXTRACT THE INFORMATION OR GIVE IT BY THE COMMAND LINE:
temp.ExtractCYSResidues(pdbfile)
#temp.ExtractCYSResidues(sys.argv[1])

disulfide_bonds = temp.GetDisulfideBonds()
for x in xrange(0, disulfide_bonds.size()):
        disulfide_bonds[x].Print()


###UPDATING CYS RESIDUES###
disulfide_bonds[0].SetIsBonded(False)
print("Updated disulfide bond(s):")
disulfide_bonds[0].Print()
temp.UpdateCYSResidues(pdbfile, disulfide_bonds)

pdbfile.Write('cysresidues-update.pdb')

