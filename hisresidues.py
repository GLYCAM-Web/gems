###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE

import gmml
import sys

temp = gmml.PdbPreprocessor()

temp.ExtractHISResidues("gmml/example/pdb/1RVZ_New.pdb")
#temp.ExtractHISResidues(sys.argv[1])

histidine_mappings = temp.GetHistidineMappings()

for x in xrange(0, histidine_mappings.size()):
        histidine_mappings[x].Print()


pdbfile = gmml.PdbFile("gmml/example/pdb/1RVZ_New.pdb")
#pdbfile = gmml.PdbFile(sys.argv[1])

###UPDATING HISTIDINE MAPPINGS###
#MODIFYING selected_mapping ATTRIBUTE OF THE HISTIDINE MAPPINGS VECTOR (POSSIBLE OPTIONS: gmml.HIE, gmml.HIP, gmml.HID)
histidine_mappings[0].SetSelectedMapping(gmml.HIP)
print "The Updated part(s):"
histidine_mappings[0].Print()
temp.UpdateHISMapping(pdbfile, histidine_mappings)

pdbfile.Write('1RVZ_New-hisresidues-update.pdb')

