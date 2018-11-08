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
import slurm

class Simulation:
    def __init__(self, SMAT_ENTRY, WEB_ID, SLURM_JOB_OBJ = None):
        self.SMAT_ENTRY = SMAT_ENTRY
        self.SLURM_JOB = SLURM_JOB_OBJ
        self.WEBID = WEB_ID
        self.RUN_PREF = conf.File_Naming.prefSTRUCTURE 
        if self.SMAT_ENTRY[SMAT.key_and_values.IONS_KEY] == SMAT.key_and_values.IONS_YES:
            self.RUN_PREF = self.RUN_PREF + conf.File_Naming.modION
        if self.SMAT_ENTRY[SMAT.key_and_values.TYPE_KEY] == SMAT.key_and_values.TYPE_SOL:
            self.RUN_PREF = self.RUN_PREF + conf.File_Naming.modSOLV
        self.LABEL = self.SMAT_ENTRY[SMAT.key_and_values.LABEL_KEY]
        self.PARMTOP = self.RUN_PREF + '.' + conf.File_Naming.extPARM
        self.INPCRD = self.RUN_PREF + '.' + conf.File_Naming.extINPCRD
        self.MDIN = self.RUN_PREF + '.' + conf.File_Naming.extMDIN
        self.MDOUT = self.RUN_PREF + '.' + conf.File_Naming.extMDOUT
        self.MDCRD = self.RUN_PREF + '.' + conf.File_Naming.extMDCRD
        self.MDRST = self.RUN_PREF + '_min.' + conf.File_Naming.extMDRST
        self.MDINFO = self.RUN_PREF + '.' + conf.File_Naming.extMDINFO
        self.MDLOG = self.RUN_PREF + '.' + conf.File_Naming.extMDLOG
        self.MD_TYPE = self.SMAT_ENTRY[SMAT.key_and_values.TYPE_KEY]
        if self.MD_TYPE == SMAT.key_and_values.TYPE_GAS:
            self.MD_DONE_TEXT = conf.MD_Defines.MD_GP_DONE_TEXT
        elif self.MD_TYPE == SMAT.key_and_values.TYPE_SOL:
            self.MD_DONE_TEXT = conf.MD_Defines.MD_SOL_DONE_TEXT

    def GetSlurmJob(self):
        if self.SLURM_JOB == None:
            print ("This simulation has not been associated with a slurm job!!!")
            return self.SLURM_JOB
        else:
            return self.SLURM_JOB

    def SetSlurmJob(self, slurm_job_obj):
        self.SLURM_JOB = slurm_job_obj

    def CreateSubmissionScript(self):
        # AMBER molecular dynamics simulation log file
        self.MDLOG = self.RUN_PREF + '.' + conf.File_Naming.extMDLOG
        #Later add in MD command for pmemd
        self.SQUEUE_NAME =  'OSM_' + self.SMAT_ENTRY[SMAT.key_and_values.LABEL_KEY]
        if self.MD_TYPE == SMAT.key_and_values.TYPE_GAS:
            self.NUM_TASKS = '1'
            self.MD_COMMAND='${AMBERHOME}/bin/sander'
            self.MD_DONE_TEXT = conf.MD_Defines.MD_GP_DONE_TEXT #Depending on solvation, this should change.Return later.
            self.MAX_TIME = '00:05:00' #For gas minimization
            gas_mdin_path = '../Min_input_files/CB_GP_Minimization_2017-01-17.mdin'
            copy_mdin = subprocess.Popen(['cp', gas_mdin_path, self.MDIN])
        elif self.MD_TYPE == SMAT.key_and_values.TYPE_SOL:
            self.NUM_TASKS = '2'
            self.MD_COMMAND='mpirun -np ' + self.NUM_TASKS + ' ${AMBERHOME}/bin/pmemd.MPI'
            self.MD_DONE_TEXT = conf.MD_Defines.MD_SOL_DONE_TEXT
            self.MAX_TIME = '01:00:00' #For solvent minimization
            sol_mdin_path = '/website/userdata/OSM_refactor/Min_input_files/CB_Sol_Minimization_2017-01-17.mdin'
            copy_mdin = subprocess.Popen(['cp', sol_mdin_path, self.MDIN])
        self.PARTITION_NAME = 'amber'
        self.NUM_NODES = '1'
        self.AMBERHOME = '/programs/amber16/'
        self.Run_Script_Name = '/' + self.RUN_PREF + '.sh'

        run_script = open(os.path.abspath(os.path.curdir) + self.Run_Script_Name, 'w+')

        script_list = [
            "#!/bin/bash\n",
            "#SBATCH -D " + os.path.abspath(os.path.curdir) + "\n",
            "#SBATCH -J " + self.SQUEUE_NAME + "\n",
            "#SBATCH --partition=" + self.PARTITION_NAME + "\n",
            "#SBATCH --get-user-env\n",
            "#SBATCH --nodes=" + self.NUM_NODES + "\n",
            "#SBATCH --tasks-per-node=" + self.NUM_TASKS + "\n",
            "#SBATCH --time=" + self.MAX_TIME + "\n\n",
            "cd " + os.path.abspath(os.path.curdir) + "\n",
            "LOGFILE=\'" + os.path.abspath(os.path.curdir) + "/global.log\'\n",
            "RUN_ID=\'" + self.WEBID + "\'\n",
            "MD_TYPE=\'" + self.MD_TYPE + "\'\n",
            "export AMBERHOME=\'" + self.AMBERHOME + "\'\n",
            "export MD_COMMAND=\"" + self.MD_COMMAND + "\"\n\n",
            "# Initialize logging for this simulation\n",
            "echo \"Beginning ${MD_TYPE} for webid ${RUN_ID} on $(date)\" >> ${LOGFILE}\n",
            "# Record the nodes that will do the calculation\n",
            "echo \"The minimization for webid ${RUN_ID} will run on these hosts:\" >> ${LOGFILE}\n",
            "srun hostname -s | sort -u >slurm.hosts\n",
            "cat slurm.hosts >> ${LOGFILE}\n",
            "# Set up and run the simulation\n",
            "source ${AMBERHOME}/amber.sh\n\n",
            "# Do the minimization\n",
            "\n",
            "${MD_COMMAND} \\\n",
            "  -p    " + self.PARMTOP + " \\\n",
            "  -c    " + self.INPCRD + " \\\n",
            "  -i    " + self.MDIN + " \\\n",
            "  -o    " + self.MDOUT +  " \\\n",
            "  -r    " + self.MDRST + " \\\n",
            "  -x    " + self.MDCRD + " \\\n",
            "  -inf  " + self.MDINFO + " \\\n",
        ]
        # Add an additional parameter if using pmemd." 
        # If not, add a blank line"
        if self.MD_TYPE == SMAT.key_and_values.TYPE_SOL:
            script_list.append("  -l    " + self.MDLOG + "\n")
        else:
            script_list.append("\n")
            
        script_list_continued = [
            "if grep -q \'" + self.MD_DONE_TEXT + "\' " + self.MDOUT + " ; then\n",
            "    echo \"Minimization of webid ${RUN_ID} appears to be complete on $(date).\" >> ${LOGFILE}\n",
            "else\n",
            "    echo \"Minimization of webid ${RUN_ID} appears to have failed on $(date).Check " + self.MDOUT + "\" >> ${LOGFILE}\n",
            "fi\n"
        ]
        script_list.extend(script_list_continued)

        run_script.writelines(script_list)
        run_script.close()

    def CheckIfCompleteFromOutputFile(self):
        MDOUT_PATH = self.LABEL + '/' + self.MDOUT
        out_str = ""
        if os.path.isfile(MDOUT_PATH) == True:
            quoted_keyword =   self.MD_DONE_TEXT 
            command = "grep " + quoted_keyword + " " + MDOUT_PATH
            check_mdout = subprocess.Popen([command], stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
            std_out, std_err = check_mdout.communicate()
            std_out_str =  std_out.decode('utf-8')
            std_err_str = std_err.decode('utf-8')
            if std_out_str != "":
                self.SLURM_JOB.status[job_status_key_values.STATUS_KEY] = job_status_key_values.STATUS_COMPLETE
                self.SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY] = SMAT.key_and_values.STATUS_COMPLETE
      
        
            
def check_if_dir_content_good(simulation_obj, SMAT_ENTRY):
    input_files_missing = False
    out_files_exist = False
    if os.path.isfile(simulation_obj.PARMTOP) == False:
        input_files_missing = True
        print('Parmtop file missing in sub directory %s'%(os.path.abspath(os.path.curdir)))
    if os.path.isfile(simulation_obj.INPCRD) == False:
        input_file_missing = True
        print('Inpcrd file missing in sub directory %s'%(os.path.abspath(os.path.curdir)))
    if os.path.isfile(simulation_obj.MDIN) == False:
        print("MDIN doesn't exist:" + simulation_obj.MDIN)
        input_file_missing = True
        print('MDIN file missing in sub directory %s'%(os.path.abspath(os.path.curdir)))
    
    if input_files_missing == True:
        log_file_name = '/global.log'
        log_file.AppendLogFile('..' + log_file_name, 'Error, one or more input files are missing in working directory: %s\n'%(os.path.abspath(os.path.curdir)) )
        simulation_obj.SLURM_JOB.status[job_status_key_values.STATUS_KEY] = job_status_key_values.STATUS_FAILED
        SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY] = SMAT.key_and_values.STATUS_FAILED
        return False

    if os.path.isfile(simulation_obj.MDOUT) == True:
        out_files_exist = True
        print('MDOUT file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
    if os.path.isfile(simulation_obj.MDCRD) == True:
        out_files_exist = True
        print('MDCRD file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
    if os.path.isfile(simulation_obj.MDINFO) == True:
        out_files_exist = True
        print('MDINFO file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
    if os.path.isfile(simulation_obj.MDLOG) == True:
        out_files_exist = True
        print('MDLOG file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
    if os.path.isfile(simulation_obj.MDRST) == True:
        out_files_exist = True
        print('MDRST file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))

    if out_files_exist == True:
        log_file_name = '/global.log'
        log_file.AppendLogFile('..' + log_file_name, 'Error, one or more output files already exist in working directory: %s\n'%(os.path.abspath(os.path.curdir)))
        simulation_obj.SLURM_JOB.status[job_status_key_values.STATUS_KEY] = job_status_key_values.STATUS_FAILED
        SMAT_ENTRY[SMAT.key_and_values.STATUS_KEY] = SMAT.key_and_values.STATUS_FAILED
        return False

    elif input_files_missing == False and out_files_exist == False:
        return True

#Later add in functions for job status query
