# Reference Materials for Test 008

Test 008 is complicated, and the 'correct outputs' used in the four sub-tests are terse.  

This directory contains materials that might be useful for troubleshooting or for understanding how the test functions.

Herein, `cb` refers to the directory at `service_path/sequence/cb`.  The value of `service_path` might change depending
on the situation.

Note that the pUUIDs in these reference directories will differ from those in any other runs of the test.

## Directory Contents

- `README.md` : this file

- `cb_final_state` : the final state of the `cb` directory tree at the end of all four tests.  
  It is important to note that the state of the `cb` directory changes after each sub-test.


- `sub-test_directory_trees` : Files containing output from the command `tree cb` at the end of each sub-test.
  These files simplify the process of figuring out which files would have been present at each stage.


## The Sub-Testts

At each stage, various subdirectories, log files, information files and symbolic links might be set.

0. Evaluation:  This sends an evaluation request.  It also builds a single default structure.
1. Build the default structure and one other.  
2. Build two structures that are not part of the initial 8 (developer) or 64 (live site) default structures.
3. Build four structures.  Two of these are new.  One of them was built in stage (sub-test) 1.  The other, in 2.


