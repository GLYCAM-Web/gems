How to run this test:
/home/yao/Documents/GLYCAM_Dev_Env/V_2/Web_Programs/gems/gemsModules/complex/glycomimetics/tasks/external_scripts_bash/master_submit.sh /home/yao/Documents/GLYCAM_Dev_Env/V_2/Web_Programs/gems/gemsModules/complex/glycomimetics/test/example_flu_3ubq_aldehyde_library

(Essentially it is: "master_submit.sh job_directory". Run from whereever most convenient for you. You don't have to provide absolute paths.)

Expected outcome:
1. "example_flu_3ubq_aldehyde_library/glycomimetics/output" should contain a list of files with *.pdb and *pdb2glycam.log
2. "example_flu_3ubq_aldehyde_library/simulation" should contain a series of directories with "analog*" and "natural"
3. "example_flu_3ubq_aldehyde_library/simulation/analog*/1_leap/" should contain several files with *.pdb and *pdb2glycam.log.
