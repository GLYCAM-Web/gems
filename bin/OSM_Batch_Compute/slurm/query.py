import subprocess
import re
import datetime
import slurm
def QueryJobStatus(job_obj_list):
    #Do a squeue -l command, but instead of using -l, explicitly specify format. 
    query = subprocess.Popen(["squeue", "-o %.18i %.9P %.8j %.8u %.8T %.10M %.9l %.6D %R"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    std_out, std_err = query.communicate()
    std_out_str =  std_out.decode('utf-8') #Is string, not list
    lines_plus_empty_str = std_out_str.split("\n")
    lines = [x for x in lines_plus_empty_str if x != '']
    line_dict_list = []

    for line in lines:
        line_dict = {}
        line_tokens_plus_empty_str = re.split("[ ]", line)
        line_tokens = [x for x in line_tokens_plus_empty_str if x != '']
        #['JOBID', 'PARTITION', 'NAME', 'USER', 'STATE', 'TIME', 'TIME_LIMI','NODES', 'NODELIST(REASON)']
        line_dict['JOBID'] = line_tokens[0]
        line_dict['PARTITION'] = line_tokens[1]
        line_dict['NAME'] = line_tokens[2]
        line_dict['USER'] = line_tokens[3]
        line_dict['STATE'] = line_tokens[4]
        line_dict['TIME'] = line_tokens[5]
        line_dict['TIME_LIMIT'] = line_tokens[6]
        line_dict['NODES'] = line_tokens[7]
        line_dict['NODELIST'] = line_tokens[8]
        line_dict_list.append(line_dict)

    line_dict_list.pop(0) # Remove the header line: 'JOBID', 'PARTITION', 'NAME', 'USER', 'STATE', 'TIME', 'TIME_LIMI','NODES', 'NODELIST(REASON)'

    running_jobs = []
    pending_jobs = []
    other_states_jobs = []
    for line_dict in line_dict_list:
        if line_dict['STATE'] == "RUNNING":
            running_jobs.append(line_dict['JOBID'])
        elif line_dict['STATE'] == "PENDING":
            pending_jobs.append(line_dict['JOBID'])
        else:
            other_states_jobs.append(line_dict['JOBID'])


    for job in job_obj_list:
        for index, line_dict in enumerate(line_dict_list):
            if job.status[slurm.job_status_key_values.JOB_ID_KEY] == line_dict['JOBID']:
                if line_dict['STATE'] == 'RUNNING':
                    job.status[slurm.job_status_key_values.STATUS_KEY] = slurm.job_status_key_values.STATUS_RUNNING
                if line_dict['STATE'] == 'PENDING':
                    job.status[slurm.job_status_key_values.STATUS_KEY] = slurm.job_status_key_values.STATUS_PENDING
                else:
                    job.status[slurm.job_status_key_values.STATUS_KEY] = slurm.job_status_key_values.STATUS_OTHER

                if len(running_jobs) == 0:
                    job.status[slurm.job_status_key_values.AHEAD_RUNNING_KEY] = '0'
                if len(pending_jobs) == 0:
                    job.status[slurm.job_status_key_values.AHEAD_WAITNG_KEY] = '0'
                if len(other_states_jobs) == 0:
                    job.status[slurm.job_status_key_values.AHEAD_OTHER_KEY] = '0'

                if job.status[slurm.job_status_key_values.STATUS_KEY] == slurm.job_status_key_values.STATUS_PENDING:
                    print("Enter1")
                    for running_count, job_id in enumerate(running_jobs, 0):
                        if job_id == job.status[slurm.job_status_key_values.JOB_ID_KEY]:
                            job.status[AHEAD_RUNNING_KEY] = str(running_count)
                    for pending_count,job_id in enumerate(pending_jobs, 0):
                        print("Enter2")
                        if job_id == job.status[slurm.job_status_key_values.JOB_ID_KEY]:
                            job.status[slurm.job_status_key_values.AHEAD_WAITING_KEY] = str(pending_count)                        
                    for other_states_count, job_id in enumerate(other_states_jobs, 0):
                        if job_id == job.status[slurm.job_status_key_values.JOB_ID_KEY]:
                            job.status[AHEAD_OTHER_KEY] = str(other_states_count)
        job.status[slurm.job_status_key_values.DATE_KEY] = datetime.date.today().strftime("%Y- %B- %d")
        job.status[slurm.job_status_key_values.TIME_KEY] = datetime.datetime.now().strftime("%H:%M:%S")
