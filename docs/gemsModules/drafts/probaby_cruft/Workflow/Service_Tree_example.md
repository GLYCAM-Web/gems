# Example of representing service nodes in bulleted list form

This is generally what a human would like to read.

In the following, numbered lists imply that the services must be run in 
sequence.  Bulleted lists can be run in parallel or, if run in serial,
can be run in any order.

0. Root of all services.
1. Validate
2. Evaluate
   1. Pre-process protein structure
   2. Evaluate requested sequences:
      - Evaluate sequence x
      - Evaluate sequence y
      - Evaluate sequence z
   3. Generate initial build time estimate
3. Build Initial Glycoprotein
   1. Build each sequence
      - Build sequence x
      - Build sequence y
      - Build sequence z
   2. Attach sequences
   3. Count clashes/atoms and generate resolution time estimate
4. Build Rotamers:
   -  Build rotamer x
   -  Build rotamer y
   -  Build rotamer z
5. Build 
