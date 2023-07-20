* structurefile is a top-level "meta"-Entity in gemsModules, containing the `PDBFile` entity. (`gemsModules.structurefile. PDBFile`)
	* PDBFile entity folder provides the `PDBFile_Entity`, it's `entitytype="PDBFile"`
		* The PDBFile Entity provides the `AmberMDPrep` Service
			* The `AmberMDPrep` Service utilizes a `prepare_pdb` Task to preprocess a pdb file with gmml.
				* `prepare_pdb` primarily wraps `ppInfo = pdbFile.PreProcess(options); pdbFile.Write(output_pdb_path)` and returns a str built from `ppInfo`.
					* The returned message is the string built from `ppInfo`.
					* A preprocessed pdb file is generated at the `output_filename` location
				* From `tests_in/explicit.json`:
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
										// Optional:
										"pUUID": "some-puuid-here", // Not currently handled.
										"inputFilsPath": "/programs/gems/tests/inputs/", // Your `PDBFile` path here. 
										"outputFilePath": "/programs/gems/tests/outputs/"  // Need to implement a more robust PDBFile fs project construction.
									}
								}
							}
						}
					}
					```
			* Tested by `gems/tests/016.test.PDBFile.sh`
				* I've provided an explicit JSON at `gems/gemsModules/structurefile/PDBFile/tests_in/explicit.json`
				* This JSON provides `inputs["input_filename"] `and `inputs["output_filename"]` to send to `prepare_pdb`
				* The service requested of the PDBFile Entity is the `AmberMDPrep` Service.
				* The "arbitrary" name of the Service Request in this JSON is `any_amber_prep`, which is simply logged by the `request_data_filler` when found.
		* Try it out with:
				./bin/delegate ./gemsModules/structurefile/PDBFile/tests_in/explicit.json \
					| $GEMSHOME/tests/utilities/json_ripper.py entity.responses.any_amber_prep.outputs.ppinfo
			* This should return the `ppInfo` string from the `prepare_pdb` Task.
			* `tests_in/_*.json` are incomplete requests and will fail.

			

> Note JSON request inputs["pdb_filename"] are currently implicitly associated with an AmberMDPrep Service Request.

### TODO
- [] Implement a more robust PDBFile fs project construction.


#### Rough Notes
- Passing inputDirPath or outputFilePath forces absolute path names, while omitting them uses Project paths.