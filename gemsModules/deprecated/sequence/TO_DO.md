Test this sequence:

    DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-2[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-4]DManpa1-3[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-2[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-6]DManpa1-6]DManpb1-4DGlcpNAcb1-4DGlcpNAcb1-OH


- [ ] Trace the progress of project creation especially directory and symboling link making
- [ ] Add "Procedural Options" to entities.  It's a place to hold info about how to do whatever.  Examples follow.  It should be possible to override these with environment variables.  Since these affect how the execution happens, then env vars get the last say. 
	- [ ] use_library : bool - if there is a library of information available, should the info there be used rather than generating new?
	- [ ] strict_library : bool - if using a library, should everything match perfectly, or can certain (determined by each entity or service) things be allowed to not match?
	- [ ] In Sequence:  build_default_on_evaluation : bool - should the default structure be built whenever a sequence is valid enough to be evaluated?  If used with "use_library=True", then a default structure is only built if one does not already exist.
	- [ ] force_serial_execution : bool - should parallel execution (spawned daemons, etc.) be disallowed.  This only applies to GEMS, not to any programs that GEMS calls.  This is useful for troubleshooting and for systems with limited resources.
	- [ ] 
- [x] Find where the request-raw and request-initialized are being written out and fix the latter
	- [x] Seems to be working now
	- [x] I changed all pydantic .json writes to use aliases EXCEPT if logging.  I left logging writes so that they use the names in the objects rather than the aliases.  I did this in sequence and in the two files in project that are used by sequence.
- [ ] Add a 'dry run' option as a feature request.  That is, a JSON object goes in and the code just sees what would happen and then returns that.  Maybe write this in a little now?
	- [x] not write now
	- [ ] add to 'procedural optons' later when implemented
	- [ ] maybe use:  https://github.com/haarcuba/dryable
- [ ] Add a link to the default structure at the top level in the Sequences/SeqID folder.  Ensure that the evaluation output is accessible.
	- [ ] Also add default link inside the build strategy folder.  That is, each build strategy gets a default but there is a default overall.
	- [ ] Ensure that the default gets built properly upon evaluation by default in a website or developer context.
	- [ ] Ensure that this can be turned off.
- [x] Also ensure that MD Minimize can be turned off.
- [ ] See if we care about structureInfoFilename being written
	- [ ] Apparently, manageSequenceBuild3DStructureRequest looks for it
- [ ] See if we care about statusFilename being written
- [ ] Generate a test input for this.  This test input might replace test 008.  And, test 008 does not need to make so many structures anyhow.
- [ ] Make the next set of to-do items for the builds...
- [ ] Set a sybolic link inside the Sequence directory to the default structure's directory
- [ ] Figure out why structures that are not "defaults" aren't being built.





- [x] When requesting an evaluation, call it that.  Stop calling it a build. 

	Done in GEMS

- [x] Add a "buildDefaultStructure" option to the Evaluation Options.   

	Set to true by default in GEMS

- [x] Set mdMinimize to True

	Set to true by default in GEMS

- [x] The unminimized structure will be there at the start as always.

	The first time a sequence is evaluated, this structure will always be built.

- [x] The project ID that comes back after the build request will ALWAYS be different from the evaluation request.

	It is possible to override this (not tested), but the default is always make a new project.


