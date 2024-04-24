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

    pdb, pdbqt, json -> pdb, pdb, txt


2. It calls makedir.sh to configure working directories for MD simulation of glycomimetic compounds.
    -Required input: output of step 1
    -Output files: none
    -Side effects:


3. It calls make_simulation_scripts.sh to make necessary scripts for MD simulation:
    > now tasks/make_simulation_scripts.py which calls other helpers
    -Required input:
        -Output files from step 1
        -Configured directories from step 2.  
    -Output files:
        -This script itself does not produce output files, but it produces simulation scripts used in the next step.


4. it calls master_submit.sh
    -Required input:
        -Simulation scripts from step 3 (Refer to the 4 scripts made)
    -Call Slurm to submit 
        - MD simulations (GEMS - use MDaaS)
        - MM-GBSA analysis (How? prob task script for now, but might be it's own Service in the future.)
    -Output files: 
        -This script itself does not produce output files, but the MD simulations it submits do create output files. 


5. It calls master_analysis.sh to analyze MD and MM-GBSA results.
    -Required input:
        -Simulation output files from step 4. 
    -Output files:
        -The script itself creates some text files that stores output values, and also prints out the most important stuff to STDOUT. 
        -Once integrated into GEMS, these should probably go into a JSON file. 

---

### Thoughts on converting these steps to services:

[See workflow](workflow.md)

- Steps 1, 3, and 4 should all belong to the Build service.
- Step 2 should belong to the ProjectManagement service.
    => PM service will need to be implicitly requested by the Build service.
- Step 5 should belong to the Analyze service.
    => Analyze cannot be requested without a valid project from a build first.


[See notes on external programs for information about tasks as well](reference/external_programs.md)
> GEMS tasks in Python will likely only wrap the shell scripts which generate other shell scripts.
> See tasks_reference/external_scripts_bash/ for the original shell scripts.