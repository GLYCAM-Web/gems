* structurefile is a top-level "meta"-Entity in gemsModules, containing the `PDBFile` entity. (`gemsModules.structurefile. PDBFile`)
	* PDBFile entity folder provides the `PDBFile_Entity`, it's `entitytype="PDBFile"`
		* The PDBFile Entity provides the `AmberMDPrep` Service
			* The `AmberMDPrep` Service utilizes a `prepare_pdb` Task to preprocess a pdb file with gmml.
				* `prepare_pdb` takes an `input_filename` and `output_filename` of `str` types(defaults to `./preprocessed.pdb`)
				* `prepare_pdb` primarily wraps `ppInfo = pdbFile.PreProcess(options); pdbFile.Write(output_pdb_path)` and returns a str built from `ppInfo`.
					* The returned message is the string built from `ppInfo`.
					* A preprocessed pdb file is generated at the `output_filename` location
			* Tested by `gems/tests/016.test.PDBFile.sh`
				* I've provided an explicit JSON at `gems/gemsModules/structurefile/PDBFile/tests_in/explicit.json`
				* This JSON provides `inputs["input_filename"] `and `inputs["output_filename"]` to send to `prepare_pdb`
				* The service requested of the PDBFile Entity is the `AmberMDPrep` Service.
				* The "arbitrary" name of the Service Request in this JSON is `any_amber_prep`, which is simply logged by the `request_data_filler` when found.
		* 
			Try it out with:
				./bin/delegate ./gemsModules/structurefile/PDBFile/tests_in/explicit.json \
					| $GEMSHOME/tests/utilities/json_ripper.py entity.responses.any_amber_prep.outputs.message