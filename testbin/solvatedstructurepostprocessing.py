import sys
sys.path.insert(0, '../')
import gmml
import time

assembly = gmml.Assembly()
assembly.BuildAssemblyFromPdbFile(sys.argv[1])
assembly.BuildStructureByDistance(1)
assembly.Solvation(10, 3, sys.argv[2])
pdb_file = assembly.BuildPdbFileStructureFromAssembly()
pdb_file.Write('solvated.pdb')
solvent = gmml.Assembly()
solute = gmml.Assembly()
assembly.SplitSolvent(solvent, solute)
llc_solvent = gmml.Coordinate()
urc_solvent = gmml.Coordinate()
solvent.GetBoundary(llc_solvent, urc_solvent)
llc_solute = gmml.Coordinate()
urc_solute = gmml.Coordinate()
solute.GetBoundary(llc_solute, urc_solute)
solvent_box_size = urc_solvent
solvent_box_size - llc_solvent
print 'Solvent box size: ' + str(solvent_box_size.GetX()) + ' x ' + str(solvent_box_size.GetY()) + ' x ' + str(solvent_box_size.GetZ())
k = [solvent_box_size.GetX(), solvent_box_size.GetY(), solvent_box_size.GetZ()]
k = sorted(k)
maxlimit = k[0] + (k[0]*0.1)
minlimit = k[0] - (k[0]*0.1)
if k[1]>minlimit and k[1]<maxlimit and k[2]>minlimit and k[2]<maxlimit:
    print ('Cubic')
else:
    print ('Rectangular')
urc_buffer = urc_solvent
urc_buffer - urc_solute
llc_buffer = llc_solute
llc_buffer - llc_solvent
l = [urc_buffer.GetX(), urc_buffer.GetY(), urc_buffer.GetZ(), llc_buffer.GetX(), llc_buffer.GetY(), llc_buffer.GetZ()]
print 'Buffer size => +X: ' + str(urc_buffer.GetX()) + ' +Y: ' + str(urc_buffer.GetY()) + ' +Z: ' + str(urc_buffer.GetZ()) + ' -X: ' + str(llc_buffer.GetX()) + ' -Y: ' + str(llc_buffer.GetY()) + ' -Z: ' + str(llc_buffer.GetZ())
m = [8, 10, 12]
solvation_size = min(m, key=lambda x:abs(x-min(l)))
print (solvation_size)
