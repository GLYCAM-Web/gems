import sys
sys.path.insert(0, '../')
import gmml
import time

assembly = gmml.Assembly()
assembly.BuildAssemblyFromPdbFile(sys.argv[1])
assembly.BuildStructureByDistance(1)
assembly.Solvation(8, 3, sys.argv[2])
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
urc_buffer = urc_solvent
urc_buffer - urc_solute
llc_buffer = llc_solute
llc_buffer - llc_solvent
print 'Buffer size => +X: ' + str(urc_buffer.GetX()) + ' +Y: ' + str(urc_buffer.GetY()) + ' +Z: ' + str(urc_buffer.GetZ()) + ' -X: ' + str(llc_buffer.GetX()) + ' -Y: ' + str(llc_buffer.GetY()) + ' -Z: ' + str(llc_buffer.GetZ())
