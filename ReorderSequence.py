
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

import gmml

sequence="LFrupa2-6-DGlcpAa1-OME"
try: 
    cond_seq=gmml.CondensedSequence(sequence) 
except:
    print("something went wrong")

print("still here")



#std::cout << "Output longest is: " << cond_seq.BuildLabeledCondensedSequence(
#		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LONGEST_CHAIN, 
#		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LONGEST_CHAIN, 
#		    false) << std::endl;
#std::cout << "Output lowest index is: " << cond_seq.BuildLabeledCondensedSequence(
#		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
#		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
#		    false) << std::endl;
#std::cout << "Output lowest index Labeled is: " << cond_seq.BuildLabeledCondensedSequence(
#		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
#		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
#		    true) << std::endl;
