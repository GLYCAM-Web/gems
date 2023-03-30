Test this sequence:

DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-2[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-4]DManpa1-3[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-2[DNeup5Aca2-6DGalpb1-4DGlcpNAcb1-6]DManpa1-6]DManpb1-4DGlcpNAcb1-4DGlcpNAcb1-OH





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



- [ ] Set a sybolic link inside the Sequence directory to the default structure's directory




- [ ] Figure out why structures that are not "defaults" aren't being built.

