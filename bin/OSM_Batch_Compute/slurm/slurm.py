#Import system packages
import subprocess
import json
import os
import sys
#Import custom packages
import conf
import SMAT
import log_file
import job_status_json
import query
import job_status_key_values
import simulation

class Slurm_Job:
    def __init__(self, SMAT_ENTRY, WEB_ID, SIMULATION_OBJ = None):
        self.SIMULATION_JOB = SIMULATION_OBJ
        self.status = {
            job_status_key_values.LABEL_KEY: '',
            job_status_key_values.DATE_KEY: '',
            job_status_key_values.TIME_KEY: '',
            job_status_key_values.TYPE_KEY: '',
            job_status_key_values.JOB_ID_KEY: '',
            job_status_key_values.MESSAGE_KEY: '',
            job_status_key_values.ERROR_KEY: '',
            job_status_key_values.QUEUE_KEY: '',
            job_status_key_values.STATUS_KEY: '',
            job_status_key_values.AHEAD_RUNNING_KEY: '',
            job_status_key_values.AHEAD_WAITING_KEY: '',
            job_status_key_values.AHEAD_OTHER_KEY: '',
            job_status_key_values.ELAPSED_KEY: '',
            job_status_key_values.TIME_REMAINING_KEY: '',
            job_status_key_values.STDOUT_KEY: '',
            job_status_key_values.STDERR_KEY: '',
            job_status_key_values.TEST_RESULT_KEY: '',
            job_status_key_values.REASON_KEY: ''
        }
        self.status[job_status_key_values.LABEL_KEY] = SMAT_ENTRY[SMAT.key_and_values.LABEL_KEY]
        self.status[job_status_key_values.TYPE_KEY] = SMAT_ENTRY[SMAT.key_and_values.TYPE_KEY]
        self.WEBID = WEB_ID
        self.job_status_json_obj = None
        self.RUN_PREF = conf.File_Naming.prefSTRUCTURE
        self.Run_Script_Name = None

    def GetSimulationJob(self):
        if self.SIMULATION_JOB == None:
            print("This slurm job object does not have a simulation job associated.")
            return None
        else:
            return self.SIMULATION_JOB

    def SetSimulationJob(self, simulation_obj):
        self.SIMULATION_JOB = simulation_obj

    def SetSubmissionScript(self, run_script_name):
        self.Run_Script_Name = run_script_name

    def DumpJobStatusJsonObj(self):
        if self.job_status_json_obj == None:
            self.job_status_json_obj = json.dumps(self.status, sort_keys = True, indent = 4, separators = (',', ':'))
        else:
            print("Job status json object already exist. Has been dumped previously.")
        
    def GetJobStatusJsonObj(self):
        if self.job_status_json_obj != None:
            return self.job_status_json_obj
        else:
            print("Job status json object does not exist. Has not been dumped previously.")


def process_individual_SMAT_entry(SMAT_ENTRY, SMAT_index, web_id):
    RUN_PREF = conf.File_Naming.prefSTRUCTURE
    new_slurm_job = Slurm_Job (SMAT_ENTRY ,web_id)
    subdir_path = os.path.abspath(os.path.curdir) + '/' + SMAT_ENTRY[SMAT.key_and_values.LABEL_KEY]
    #For testing, temporary change to "STATUS_COMPLETE". Should be "STATUS_READY"
    if SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY] != SMAT.key_and_values.STATUS_READY: #If status is not "Ready", the job has been submitted before.Will not attempt re-submission.
        if SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY].find(SMAT.key_and_values.STATUS_JOBID_PREFIX) != -1: #If current job has job id, it has been submitted before. Can't decide its status at this point, could be PD,R,C etc.
            new_slurm_job.status[job_status_key_values.JOB_ID_KEY] = SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY].replace(SMAT.key_and_values.STATUS_JOBID_PREFIX,'')
        else: #If job does not have job id, it hasn't been successfully submitted before. In this case, copy the status in structure mapping table(Failed,Error etc) 
            new_slurm_job.status[job_status_key_values.STATUS_KEY] = SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY]
        new_simulation_job = simulation.Simulation(SMAT_ENTRY, web_id, new_slurm_job)
        new_slurm_job.SetSimulationJob (new_simulation_job)
        return new_slurm_job
    
    else: #If status is Ready, job needs first-time submission or resubmission.So code will attempt submission.         
        if os.path.isdir(subdir_path) == False:
            print('Error: subdirectory ' + SMAT_ENTRY[SMAT.key_and_values.LABEL_KEY] + 'does not exist.')
            new_slurm_job.status[job_status_key_values.MESSAGE_KEY] = new_slurm_job.status[job_status_key_values.MESSAGE_KEY] + ' Job submission failed for ' + SMAT_ENTRY[SMAT.key_and_values.LABEL_KEY] + '. See errors'
            new_slurm_job.status[job_status_key_values.STATUS_KEY] = job_status_key_values.STATUS_FAILED  #This line not in original bash script OSM_Do_Job_Submissions_2017-01-17.bash
        else:
            print("chdir to " + subdir_path)
            os.chdir(subdir_path)
            new_simulation_job = simulation.Simulation(SMAT_ENTRY, web_id, new_slurm_job)
            new_slurm_job.SetSimulationJob (new_simulation_job)
            new_simulation_job.CreateSubmissionScript()
            new_slurm_job.SetSubmissionScript(new_simulation_job.Run_Script_Name)
            if simulation.check_if_dir_content_good(new_simulation_job, SMAT_ENTRY) == True:
                #Submit job
                submit_check_if_success(new_slurm_job, SMAT_ENTRY)
            
            else:
                print('Directory content bad. Input files are absent or output files are present.Unable to submit job.Skip this subdirectory')

            os.chdir('..')

        return new_slurm_job

def process_SMAT_entries(SMAT_array, job_id):
    SMAT_index = -1
    job_objects_list = []
    Main_dir = os.path.abspath(os.path.curdir)
    for entry in SMAT_array:
        SMAT_index += 1
        new_slurm_job_object = process_individual_SMAT_entry(entry, SMAT_index, job_id)
        job_objects_list.append(new_slurm_job_object)

    return job_objects_list
            
def submit_check_if_success(job_obj, SMAT_ENTRY):
    print("Now submitting using script: " + job_obj.Run_Script_Name)
    slurm_submit = subprocess.Popen(['sbatch', '--output=slurm-\%j.out', '--error=slurm-\%j.err', './' + job_obj.Run_Script_Name], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print("Just submitted a job")
    #slurm_submit = subprocess.Popen(['echo', '\'testing it!!!\''], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    std_out, std_err = slurm_submit.communicate()
    std_out_str =  std_out.decode('utf-8')
    print("stdout for sub: " + std_out_str)
    if std_out_str.find('Submitted batch job') == -1:
        SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY] = SMAT.key_and_values.STATUS_FAILED
        job_obj.status[job_status_key_values.MESSAGE_KEY] = job_obj.status[job_status_key_values.MESSAGE_KEY] + ' Job submission failed for ' + job_obj.status[SMAT.key_and_values.LABEL_KEY] + '. See errors'
        job_obj.status[job_status_key_values.ERROR_KEY] = job_obj.status[job_status_key_values.ERROR_KEY] + ' Server returned:' + std_out_str
        job_obj.status[job_status_key_values.STATUS_KEY] = job_status_key_values.STATUS_FAILED
        return False
    else:
        job_obj.status[job_status_key_values.STATUS_KEY] = job_status_key_values.STATUS_SUBMITTED #Should this be "submitted", or "JID-12345"?
        job_obj.status[job_status_key_values.QUEUE_KEY] = 'testQueueName'
        #Trim "Submitted batch job 123\n" into "123". Remove "Submitted batch job" and "\n" and any whitespaces
        trimmed_std_out_str1 = std_out_str.replace('Submitted batch job ', '')
        trimmed_std_out_str2 = trimmed_std_out_str1.strip(' \n')
        SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY] = SMAT.key_and_values.STATUS_JOBID_PREFIX + trimmed_std_out_str2 
        job_obj.status[job_status_key_values.JOB_ID_KEY] = trimmed_std_out_str2
        return True

#Later add in functions for job status query
