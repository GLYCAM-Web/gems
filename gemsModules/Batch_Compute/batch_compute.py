#!/usr/bin/python3.4

import sys
import os
import subprocess

def batch_compute (web_id, workdir):

  #Create global log file
  log_file_name = '/global.log'   ## FIXME
  log_file.CreateLogFile(workdir + log_file_name)
  print("past log")   ## FIXME
  #Copy structure mapping table to shadow mapping table
  #cp_file = subprocess.Popen(['cp', conf.File_Naming.SMAP_Actual, conf.File_Naming.SMAP] )

  #Parse SMAP into internal array for use with the code
  SMAT_file_name = '/' + conf.File_Naming.SMAP_Actual
  SMAT_array = SMAT.parse(workdir + SMAT_file_name)
  print("past parse")   ## FIXME

  #Process each parsed SMAT entry. For each line, if status is ready, submit job and query status. Otherwise, just query status,either from SMAP , file status, or sbatch.
  all_job_objects = slurm.process_SMAT_entries(SMAT_array, web_id) #Note that for now, code will automatically submit viable jobs before this list in returned. Later let user submit manually.
  print("past process")   ## FIXME
  #After all SMAT entries have been processed, run a squeue command with the following function, and update job status.
  slurm.QueryJobStatus(all_job_objects)
  print("past query")   ## FIXME
  #Dump batch job status into a json file.
  batch_job_set_dict = job_status_json.BatchJobSetInfo
  batch_job_set_dict['webId'] = web_id + "\n"

  for obj in all_job_objects:
      simulation = obj.GetSimulationJob()
      if simulation != None:
          simulation.CheckIfCompleteFromOutputFile()
      obj.DumpJobStatusJsonObj()
      batch_job_set_dict['jobInfo'].append(obj.GetJobStatusJsonObj())

  json_file_name = '/test.json'   ## FIXME
  job_status_json.dump_job_set_json(batch_job_set_dict, workdir + json_file_name)
  print("past dump")   ## FIXME

  #Write shadow mapping table
  SMAT.write_shadow_SMAT(SMAT_array, workdir + '/' + conf.File_Naming.SMAP)
  print("past write")   ## FIXME


if (__name__ == '__main__'):
  import sys
  if len(sys.argv) != 3:
      print('Must supply exactly 2 arguments: batch_compute.py web_id work_dir')
      print('%d arguments are supplied'%(len(sys.argv)-1) )
      sys.exit()
  
  if os.path.isdir(sys.argv[2]) == False:
      print('Argument 2: "' + sys.argv[2] + '" is not a directory')
      sys.exit()

  batch_compute ( sys.argv[1], sys.argv[2] )

  
