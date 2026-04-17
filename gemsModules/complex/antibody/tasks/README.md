# Purpose of task files

## Python

`amber_submit.py`

	- Creates an input JSON file to be sent to `complex/amber_receive.py`
	- Does this via `manageIncomingString` but would be better if delegated\

	Variable Inputs:

        - "jobID": pUUID,
        - "localWorkingDirectory": str(projectDir),
        - "submissionName": f"ad-{pUUID}",
        - "context": "AntibodyDocking",
        - "simulationWorkingDirectory": str(projectDir),

	Possibly not used (not set or used anywhere I can find):

        - "simulationControlScriptPath": "\n".join(control_lines),
        - "simulationControlScriptArguments": " ".join(control_args) if control_args else None,

	Static Inputs:

	- "molecularSystemType": "Solvated System",
        - "molecularModelingJobType": "",
        - "dontSbatch": not sbatch,
        - "comment": "initiated by gemsModules/complex/AntibodyDocking",

`create_ad2cliconfig.py`

	- Appears to be unused.
	- If used, would generate the `ad2cliconfig` file.
        - Currently uses replacement of keywords in a template file.
	- Returns the path to the file.

	Variable Inputs: 

	- workdir (projectDir)

`create_configs.py`

	- Generates AAD2 config files: ad2config, gwconfig, vcconfig
	- Called from services/ProjectManagement/logic.py
	- Uses 'textwrap.dedent' which might not work as desired.

	Variable Inputs:

	- path - path to the file to be written
	- antibodytibody (not misspelled) - antibody file name (the pdb file) - `antibody_name`
	- glycan - name of the glycan file
	- image - name and tag for docker image to use - need to read from IC or grab from AAD2 code
	- siteversion - e.g., actual, swarmtest, etc.

	Consider for future:

	- Get most info, including generated files, from the AAD2 code.

`create_slurm_submission.py`

	- Generates the slurm submission script
	- Really should just send info to batchcompute/slurm. One day.

	Really - most of this should be in batchcompute/slurm. 
		Consider this code a work-in-progress test.

	!!! Get the other stuff written first. 
	!!! There are lots of little variables, some hidden in dictionaries.

`fix_glycam_glycan.py`

	- Ensures that there is an 'END' card at the end of a PDB file.

	Variable Inputs:

	- `glycan_path` - path to the glycan file that might need an END card.

`get_services_list.py`

	- Standard service to list available services.

	No needed variables and probably no changes either.

`run_ad_build.py`

	- Runs `run_ad_build.sh`.

	Variable Inputs:

	- `project_dir`
	- `use_serial`

	Runs the build as a subprocess.

`run_ad_evaluate.py`

	- Runs `run_ad_evaluate.sh`.

	Variable Inputs:

	- pUUID
	- `project_dir`
	- `use_serial`

	Runs evaluate as a subprocess.

`run_detect_sugars.py`

	- Runs the `detect_sugars.exe` binary.

	Variable Inputs:

	- GEMSHOME
	- `pdb_path` - path to the pdb file containing the glycan.
	- workdir - project directory

`set_up_build_directory.py`

	- Appears to be unused. The execute function contains only 'pass'.
	- Possibly, the functions this would have had are performed by services/ProjectManagement.

	Tag for deletion if truly unused.

`update_build_options.py`

	- Changes user-specified build options in the relevant config files.

	Variable Inputs:

	- workdir - project directory 
	- options - dictionary of options to change in the ad2config file.


## BASH

`run_ad_build.sh`

	- Runs `AD_Prep_Glycan` followed by `submit_and_spawn_monitor`

	Variable Inputs:

		Environment Variables:

		- WD
		- `AAD2_CLI_BIN_PATH`
		- `AAD2_DOCKER_HOME`

`run_ad_evaluate.sh`

	- Runs `AD_Evaluate`.

	Variable Inputs:

		Environment Variables:

		- WD
		- `AAD2_CLI_BIN_PATH`
		- `AAD2_DOCKER_HOME`


