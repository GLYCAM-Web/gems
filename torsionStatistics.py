### Disaccharide pattern:  [isomer: D/L][mono_condensed_name][ring_type: p/f][configuration: a/b/x][link_index]-[link_index][isomer: D/L][mono_condensed_name][ring_type: p/f][isomer: a/b/x]
import sys
sys.path.insert(0, '/home/delaram/Projects/gems')
import gmml
temp = gmml.Assembly()

temp.CalculateTorsionStatistics(sys.argv[1], -180, 180)

