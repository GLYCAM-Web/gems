###FOR FURTHER INSTRUCTIONS PLEASE REFER TO alternateresidues.py SAMPLE FILE
#SAMPLE COMMAND :
# python cycle.py -amino_libs "gmml/dat/CurrentParams/leaprc.ff12SB_2014-04-24/amino12.lib" -pdb "../../Downloads/1.pdb" &> output_file_name


import gmml
import sys
import time
import os

def main():
	het = gmml.string_vector()
	amino_libs = gmml.string_vector()
	pdb_file = ''
	if len(sys.argv) < 2:
		print 'Please import one pdb file using -pdb option and (optionally) amino library file(s) using -amino_libs option'
	elif sys.argv[1] == '-amino_libs': 
		arguments = sys.argv[2].split(',')
		for argument in arguments:
			amino_libs.push_back(argument)
		if len(sys.argv) < 4:
			print 'Please import one pdb file using -pdb option'
		elif sys.argv[3] == '-pdb':
			pdb_file = sys.argv[4]
	elif sys.argv[1] == '-pdb':
		pdb_file = sys.argv[2]
		if len(sys.argv) > 3:
			if sys.argv[3] == '-amino_libs':
				arguments = sys.argv[4].split(',')
				for argument in arguments:
					amino_libs.push_back(argument)
	#het.push_back("../../Downloads/DAldoHexaF/DGlcfb.pdb")
	#het.push_back("../../Downloads/glycam_gg_gg_gg_gg.pdb")
	#het.push_back("../../Downloads/1 (7).pdb")
	#het.push_back("../../Downloads/1 (7).pdb")
	#het.push_back("../../Documents/PDB/4A2G.pdb")
	#het.push_back("../../Documents/PDB/1G1Y.pdb")
	#het.push_back("../../Documents/PDB/1RVZ.pdb")
	#het.push_back("../../Documents/PDB/3C43.pdb")
	#het.push_back("../../Documents/PDB/6CPP.pdb")
	#het.push_back("../../Documents/PDB/1DMT.pdb")
	#het.push_back("../../Documents/PDB/1G45.pdb")
	#het.push_back("../../Documents/PDB/4HJL.pdb")
	#het.push_back("../../Documents/PDB/4OBR.pdb")
	#het.push_back("../../Documents/PDB/1KC3.pdb")
	#het.push_back("../../Documents/PDB/4A2G_test.pdb")    	#C-N-CO-C with anomeric checked!
	#het.push_back("../../Documents/PDB/4A2G_test-1.pdb")	#C-N-CO-C without anomeric checked!
	#het.push_back("../../Documents/PDB/4A2G_test-2.pdb")	#C-N-CO-CO with anomeric checked!
	#het.push_back("../../Documents/PDB/4A2G_test-3.pdb")	#CH-N , C-(O,O) without anomeric checked!
	#het.push_back("../../Documents/PDB/4A2G_test-4.pdb")	#C-N-C with anomeric checked!
	#het.push_back("../../Documents/PDB/4A2G_test-5.pdb")	#C-N-C with anomeric checked!

	if pdb_file != '':
		het.push_back(pdb_file)
		temp = gmml.Assembly(het, gmml.PDB)
		empty = gmml.string_vector()
		start = time.time()
		temp.BuildStructureByDistance(10)
		#def calculateDistanceThread(all_atoms_of_assembly, fraction_of_atoms):

		#temp = buildStructureByDistancePython(1.65, 0, temp)

		#temp.Print()
		end = time.time()
		print end - start
		#temp.Print()
		temp.ExtractSugars(amino_libs)		
#	os.system('curl -g -H "Accept: application/json" "http://localhost:8890/sparql" --data-urlencode "query=SELECT ?a where { ?a rdf:type owl:Class}"')

def buildStructureByDistancePython(cutoff, model_index, temp):
	print 'Python: Building structure by distance ...'
	model_index_ = model_index	
	all_atoms_of_assembly = temp.GetAllAtomsOfAssembly();

	i = 0
	for x in xrange(0, all_atoms_of_assembly.size()-1):
#	    all_atoms_of_assembly[x].Print()
	    print 'x is: ', x
	    atom = gmml.Atom()
	    atom = all_atoms_of_assembly[x]
	    atom_node = gmml.AtomNode()
	    atom_vector = atom_node.GetNodeNeighbors()
	    if atom.GetNode() is None:
			atom_node.SetAtom(atom);
	    else:
			atom_node = atom.GetNode()			
	    atom_node.SetId(i)
	    i = i+1
	    for y in xrange(x+1, all_atoms_of_assembly.size()):
			print 'y is: ', y
			neighbor = gmml.Atom()
			neighbor = all_atoms_of_assembly[y]
			neighbor_node = gmml.AtomNode()
			neighbor_vector = neighbor_node.GetNodeNeighbors()
			if temp.CalculateDistance(atom, 0, neighbor):
				print 'bond! '
				if neighbor.GetNode() is None:
					neighbor_node.SetAtom(neighbor)
				else:
					neighbor_node = neighbor.GetNode()
				print 'about to add node neighbor to atom node: ', atom_node
#				atom_node.AddNodeNeighbor(neighbor)
				atom_vector.push_back(neighbor)
				print 'atom node added node neighbor: ', neighbor.GetName()
#				neighbor_node.AddNodeNeighbor(atom)
				neighbor_vector.push_back(atom)
				neighbor_node.SetNodeNeighbors(neighbor_vector)
				neighbor.SetNode(neighbor_node)
				print 'END'
	    print 'Atom Vector ', atom_vector
	    print 'Atom Node ', atom_node.GetNodeNeighbors() 
	    atom_node.SetNodeNeighbors(atom_vector)
#	    atom.SetNode(atom_node)
#	    print 'node set for atom and node is', atom.GetNode() 
#	    print 'atom for the node is', atom_node.GetAtom() 
	return temp    


if __name__ == '__main__':
	main()
