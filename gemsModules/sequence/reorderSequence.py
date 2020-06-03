import gmml

    sequence = string_from_somewhere

    gmml.CondensedSequenceSpace.CondensedSequence cond_seq(sequence)

    LongestChainVersion = cond_seq.BuildLabeledCondensedSequence(
		    gmml.CondensedSequenceSpace.CondensedSequence.Reordering_Approach.LONGEST_CHAIN, 
		    gmml.CondensedSequenceSpace.CondensedSequence.Reordering_Approach.LONGEST_CHAIN, 

		    cond_seq.Reordering_Approach.LONGEST_CHAIN, 

		    false) 



    std::cout << "Output lowest index is: " << cond_seq.BuildLabeledCondensedSequence(
		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
		    false) << std::endl;
    std::cout << "Output lowest index Labeled is: " << cond_seq.BuildLabeledCondensedSequence(
		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
		    CondensedSequenceSpace::CondensedSequence::Reordering_Approach::LOWEST_INDEX, 
		    true) << std::endl;
