###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE

import sys
sys.path.insert(0, '../')
import gmml

temp = gmml.PdbPreprocessor()
st = gmml.PdbFile()
pdbfile = st.LoadPdbFile("gmml/example/pdb/1RVZ_New.pdb")
#pdbfile = gmml.PdbFile(sys.argv[1])

temp.ExtractHISResidues(pdbfile)

histidine_mappings = temp.GetHistidineMappings()

for x in xrange(0, histidine_mappings.size()):
        histidine_mappings[x].Print()

###UPDATING HISTIDINE MAPPINGS###
#MODIFYING selected_mapping ATTRIBUTE OF THE HISTIDINE MAPPINGS VECTOR (POSSIBLE OPTIONS: gmml.HIE, gmml.HIP, gmml.HID)
histidine_mappings[0].SetSelectedMapping(gmml.HIP)
print("The Updated part(s):")
histidine_mappings[0].Print()
temp.UpdateHISMapping(pdbfile, histidine_mappings)

pdbfile.Write('hisresidues-update.pdb')

