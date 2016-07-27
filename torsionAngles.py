### Disaccharide pattern:  [isomer: D/L][mono_condensed_name][ring_type: p/f][configuration: a/b/x][link_index]-[link_index][isomer: D/L][mono_condensed_name][ring_type: p/f][isomer: a/b/x]
import sys
sys.path.insert(0, '../')
import gmml
temp = gmml.Assembly()


#temp.ExtractAtomCoordinatesForTorsionAnglesFromOntologySlow("DNeupNAca2-3DGalpb")
temp.ExtractAtomCoordinatesForTorsionAnglesFromOntologySlow("DNeupNAca2-6DGalpb")
temp.ExtractTorsionAnglesFromSlowQueryResult()

#temp.ExtractAtomCoordinatesForTorsionAnglesFromOntologyFast("DNeupNAca2-3DGalpb")
#temp.ExtractTorsionAnglesFromFastQueryResult()
