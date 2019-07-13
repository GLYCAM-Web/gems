#include "../../gmml/includes/gmml.hpp"
#include "../../gmml/includes/MolecularModeling/assembly.hpp"
#include "../../gmml/includes/ParameterSet/PrepFileSpace/prepfile.hpp"
#include "../../gmml/includes/ParameterSet/PrepFileSpace/prepfileresidue.hpp"
#include "../../gmml/includes/ParameterSet/PrepFileSpace/prepfileprocessingexception.hpp"
#include "../../gmml/includes/ParameterSet/OffFileSpace/offfile.hpp"
#include "../../gmml/includes/ParameterSet/OffFileSpace/offfileresidue.hpp"
#include "../../gmml/includes/ParameterSet/OffFileSpace/offfileprocessingexception.hpp"
#include <iostream>
#include <string>

int main(int argc, char *argv[])
{
    char USAGE[] = "USAGE:\n    executable PrepFile sequence OffFileName PDBFileName";
    if(argc<5) {
	    printf("\nIncorrect number of arguments.\n");
	    printf("%s\n", USAGE);
	    printf("\nExiting.\n");
	    exit(1);
    }
    std::string prep = argv[1];
    PrepFileSpace::PrepFile* prepA = new PrepFileSpace::PrepFile(prep);
    std::string condensed_sequence = argv[2];
    MolecularModeling::Assembly assemblyA = MolecularModeling::Assembly();
    assemblyA.SetName("CONDENSEDSEQUENCE");
    assemblyA.BuildAssemblyFromCondensedSequence (condensed_sequence, prepA);
    assemblyA.CreateOffFileFromAssembly(argv[3],0);
    PdbFileSpace::PdbFile *outputPdbFile = assemblyA.BuildPdbFileStructureFromAssembly();
    outputPdbFile->Write(argv[4]);

    return 0;
} 
