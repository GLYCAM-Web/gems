Test this sequence:

    DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-2[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-4]DManpa1-3[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-2[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-6]DManpa1-6]DManpb1-4DGlcpNAcb1-4DGlcpNAcb1-OH


- [ ] Trace the progress of project creation especially directory and symboling link making
- [x] Find where the request-raw and request-initialized are being written out and fix the latter
	- [ ] Seems to be working now
- [ ] Add a 'dry run' option as a feature request.  That is, a JSON object goes in and the code just sees what would happen and then returns that.  Maybe write this in a little now?
- [ ] Add a link to the default structure at the top level in the Sequences/SeqID folder.  Ensure that the evaluation output is accessible.
- [ ] Ensure that the default gets built properly upon evaluation by default.
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


