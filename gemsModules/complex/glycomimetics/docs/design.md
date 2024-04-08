The glcomimetics tool performs the following tasks in the order they are mentioned:

1. It calls a C++ program to build glycomimetic compounds in silico
    -Required input from website/gems: 
        -A PDB input file containing a co-complex between a receptor protein and a carbohydrate ligand. 
        -A json file specifying all the parameters that control all the details of this job. 
    -Required metadata:
        -A library of pre-built drug-like moieties, in the format of PDBQT.
    -Output files (for each glycomimetic compound):
        -A PDB file for the receptor
        -A PDB file for the glycomimetic ligand.
        -A text file recording Pdb2Glycam matching results. 

2. It calls makedir.sh to configure working directories for MD simulation of glycomimetic compounds.
    -Required input: output of step 1
    -Output files: none

3. It calls make_simulation_scripts.sh to make necessary scripts for MD simulation:
    -Required input:
        -Output files from step 1
        -Configured directories from step 2.  
    -Call Slurm to submit MD simulations and MM-GBSA analysis.
        -My scripts can submit MD simulations in the machine they are being run.
        -If the MD jobs must happen on different machines, I will need to invoke MDaaS. 
    -Output files: 
        -This script itself does not produce output files, but the MD simulations it submits do contain output files. 

4. It calls master_analysis.sh to analyze MD and MM-GBSA results.
    -Required input:
        -Simulation output files from step 3. 
    -Output files:
        -The script itself creates some text files that stores output values, and also prints out the most important stuff to STDOUT. 
        -Once integrated into GEMS, these should probably go into a JSON file. 
