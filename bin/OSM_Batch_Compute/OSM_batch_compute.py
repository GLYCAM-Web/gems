#!/usr/bin/python3.4

import sys
import os
import subprocess

#Add all custom modules to sys path, to enable cyclic imports.
curdir_absolute_path = os.path.abspath(os.path.curdir)
sys.path.append(curdir_absolute_path + '/conf')
sys.path.append(curdir_absolute_path + '/slurm')
sys.path.append(curdir_absolute_path + '/log')
sys.path.append(curdir_absolute_path + '/SMAT')
sys.path.append(curdir_absolute_path + '/job_status_json')
sys.path.append(curdir_absolute_path + '/simulation')

import log_file
import conf
import SMAT
import slurm
import job_status_json

#Argument handling, make sure it's "OSM_Batch_Compute.py web_id work_dir"
if len(sys.argv) != 3:
    print('Must supply exactly 2 arguments: OSM_Batch_Compute.py web_id work_dir')
    print('%d arguments are supplied'%(len(sys.argv)-1) )
    sys.exit()

elif os.path.isdir(sys.argv[2]) == False:
    print('Argument 2 is not a directory')
    sys.exit()

web_id = sys.argv[1]
workdir = sys.argv[2]

#Create global log file
log_file_name = '/global.log'
log_file.CreateLogFile(workdir + log_file_name)
print("past log")
#Copy structure mapping table to shadow mapping table
#cp_file = subprocess.Popen(['cp', conf.File_Naming.SMAP_Actual, conf.File_Naming.SMAP] )

#Parse SMAP into internal array for use with the code
SMAT_file_name = '/' + conf.File_Naming.SMAP_Actual
SMAT_array = SMAT.parse(workdir + SMAT_file_name)
print("past parse")

#Process each parsed SMAT entry. For each line, if status is ready, submit job and query status. Otherwise, just query status,either from SMAP , file status, or sbatch.
all_job_objects = slurm.process_SMAT_entries(SMAT_array, web_id) #Note that for now, code will automatically submit viable jobs before this list in returned. Later let user submit manually.
print("past process")
#After all SMAT entries have been processed, run a squeue command with the following function, and update job status.
slurm.QueryJobStatus(all_job_objects)
print("past query")
#Dump batch job status into a json file.
batch_job_set_dict = job_status_json.BatchJobSetInfo
batch_job_set_dict['webId'] = web_id + "\n"

for obj in all_job_objects:
    simulation = obj.GetSimulationJob()
    if simulation != None:
        simulation.CheckIfCompleteFromOutputFile()
    obj.DumpJobStatusJsonObj()
    batch_job_set_dict['jobInfo'].append(obj.GetJobStatusJsonObj())

json_file_name = '/test.json'
job_status_json.dump_job_set_json(batch_job_set_dict, workdir + json_file_name)
print("past dump")

#Write shadow mapping table
SMAT.write_shadow_SMAT(SMAT_array, workdir + '/' + conf.File_Naming.SMAP)
print("past write")

