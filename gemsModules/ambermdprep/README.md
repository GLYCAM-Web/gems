* AmberMDPrep is a top-level Entity in gemsModules, named `ambermdprep` (`gemsModules.ambermdprep`)
	* ambermdprep entity folder provides the `AmberMDPrep_Entity`, it's `entitytype="AmberMDPrep"`
		* The AmberMDPrep Entity provides the `PreparePDB` Service
			* The `PreparePDB` Service utilizes a `prepare_pdb` Task (Note: prepare_pdb is the name of the PreparePDB Service folder, but `PreparePDB` is the Service `typename`.)
				* `prepare_pdb` takes an `input_filename` and `output_filename` of `str` types(defaults to `./preprocessed.pdb`)
				* `prepare_pdb` primarily wraps `ppInfo = pdbFile.PreProcess(options); pdbFile.Write(output_pdb_path)` and returns a str built from `ppInfo`.
					* The returned message is the string built from `ppInfo`.
					* A preprocessed pdb file is generated at the `output_filename` location
			* I've provided an explicit JSON input which uses the same test pdb that Oliver used.
				* This JSON looks for `inputs["input_filename"] `and `inputs["output_filename"]` to send to `prepare_pdb`
				* The service requested of the AmberMDPrep Entity is the `PreparePDB` Service.
				* The "arbitrary" name of the Service Request in this JSON is `any_amber_prep`, which is simply logged by the `request_data_filler` when found.
		* Tested by `gems/tests/016.test.AmberMDPrep.sh`