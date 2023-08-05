* structurefile is a top-level "meta"-Entity in gemsModules, containing the `PDBFile` entity. (`gemsModules.structurefile.PDBFile`)
	* PDBFile entity folder provides the `PDBFile_Entity`, it's `entitytype="PDBFile"`
		* The PDBFile Entity provides the `AmberMDPrep` and `ProjectManagement`Services. (PM - tentatively)
			* The `AmberMDPrep` Service utilizes a `prepare_pdb` Task to preprocess a pdb file with gmml.
				* `prepare_pdb` primarily wraps `ppInfo = pdbFile.PreProcess(options); pdbFile.Write(output_pdb_path)` and returns a str built from `ppInfo`.
					* The returned message is the string built from `ppInfo`.
					* A preprocessed pdb file is generated at the `output_filename` location
				* From `tests_in/explicit_test.json`:
					```json
					{
						"entity": {
							"type": "PDBFile", // Requesting the PDBFile Entity
							"services": {
								"any_amber_prep": { // Your arbitrary name for this service request.
									"type": "AmberMDPrep", // Requesting the AmberMDPrep Service
									"inputs": {
										"action": "preprocess", // Not currently handled.
										// Currently, 'pdb_filename' is preprocessed by default
										"pdb_filename": "016.AmberMDPrep.4mbzEdit.pdb", 
										"pUUID": "some-puuid-here", // Not currently handled.
										// TODO: handle arbitrary input paths and copy to project directory
										"inputFilePath": "/programs/gems/tests/inputs/", // Your `PDBFile` path here. 
										// Optional, if not passed write to the project directory.
										"outputFilePath": "/programs/gems/tests/outputs/"  // Need to implement a more robust PDBFile fs project construction.
									}
								}
							}
						}
					}
					```
				* Tested by `gems/tests/016.test.PDBFile.sh`
					* I've provided an explicit JSON at `gems/gemsModules/structurefile/PDBFile/tests_in/explicit_test.json`
				* Try it out with:
					./bin/delegate ./gemsModules/structurefile/PDBFile/tests_in/explicit_test.json \
						| $GEMSHOME/tests/utilities/json_ripper.py entity.responses.any_amber_prep.outputs.ppinfo
				* This should return the `ppInfo` string from the `prepare_pdb` Task.
				* `tests_in/_*.json` are incomplete requests and will fail.
				
			* `ProjectManagement`is service meant to be typically implied by other services or entities which require project directory management at Service Request execution time.
				* In `PDBFile.workflow_manager.Service_Dependencies`, `AmberMDPrep` is configured to depend on `ProjectManagement`. This means that `ProjectManagement`'s Servicer will serve before AmberMDPrep, ensuring the project directory and any project files are created for AmberMDPrep.
					* For now, see `common.code_utils.resolve_dependency_list` for implementation details on service resolution. (really trivial at the moment!)
			

> Note the JSON request field `inputs["pdb_filename"]` is currently implicitly associated with an AmberMDPrep Service Request. That is to say, if the PDBFile entity gets a pdb_filename input, it will run AmberMDPrep on it. 

### TODO
- [x] Implement a more robust PDBFile fs project construction.
	- [x] Use gems project manager to instantiate project
	- [x] Write preprocessed pdb file to project directory

- [x] copy upload file from an "arbitrary" upload path to project directory before servicing
- [x] copy json request to project directory
- [] write project specific logs to project directory


## A Note on Function

When one requests the `AmberMDPrep`service from `PDBFile`, it's Workflow Manager will figure out that `AmbermDPrep` requires the `ProjectManagement` service to instantiate the project environment for the AmberMDPrep request. 

`PDBFile`'s data request filler will use the requesting AAOP's ID_String to find appropriate inputs that need to be passed from the explicit service requests to any implicit ones. For instance, The input pdb file that AmberMDPrep is given can be uploaded anywhere, but ProjectManagement, by inspecting it's requester's inputs, can also copy the resources AmberMDPrep needs to the project directory.

AAOP.Dependencies isn't used to solve dependencies, rather, resolved dependency `AAOP.ID_String`s get appended so they can be easily accessed at runtime.

workflow_manager.Service_Dependencies currently configures the dependency ordering. This might belong in settings.Omitted services are assumed to have no other dependencies.

#### Rough Notes
- Passing inputDirPath or outputFilePath forces absolute path names, while omitting them uses Project paths. 