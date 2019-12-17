#custom
import conf
class Amber_Job:
    def __init__(self, json_dict):
	#Job id
        self.JobId = json_dict['job_id']
        self.WorkDir = json_dict['workingDirectory']
        
        #File names
        self.RUN_PREF = conf.File_Naming.prefSTRUCTURE + conf.File_Naming.modION + conf.File_Naming.modSOLV
        self.PARMTOP = self.RUN_PREF + '.' + conf.File_Naming.extPARM
        self.INPCRD = self.RUN_PREF + '.' + conf.File_Naming.extINPCRD
        #input file names
        self.MININ = self.RUN_PREF + '.' + conf.File_Naming.extMININ
        self.HEATIN = self.RUN_PREF + '.' + conf.File_Naming.extHEATIN
        self.EQUIIN = self.RUN_PREF + '.' + conf.File_Naming.extEQUIIN
        self.MDIN = self.RUN_PREF + '.' + conf.File_Naming.extMDIN
        #output file names
        self.MINOUT = self.RUN_PREF + '.' + conf.File_Naming.extMINOUT
        self.HEATOUT = self.RUN_PREF + '.' + conf.File_Naming.extHEATOUT
        self.EQUIOUT = self.RUN_PREF + '.' + conf.File_Naming.extEQUIOUT
        self.MDOUT = self.RUN_PREF + '.' + conf.File_Naming.extMDOUT
        #coordinate file names
        self.MINRST = self.RUN_PREF + '_min.' + conf.File_Naming.extMDRST # single frame coordinate file
        self.HEATRST = self.RUN_PREF + '_heat.' + conf.File_Naming.extMDRST # single frame coordinate file
        self.EQUIRST = self.RUN_PREF + '_equi.' + conf.File_Naming.extMDRST # single frame coordinate file
        self.MDRST = self.RUN_PREF + '_md.' + conf.File_Naming.extMDRST # single frame coordinate file
        #trajectory file_names
        self.MINCRD = self.RUN_PREF + '.' + conf.File_Naming.extMINCRD
        self.HEATCRD = self.RUN_PREF + '.' + conf.File_Naming.extHEATCRD
        self.EQUICRD = self.RUN_PREF + '.' + conf.File_Naming.extEQUICRD
        self.MDCRD = self.RUN_PREF + '.' + conf.File_Naming.extMDCRD # MD production run trajectory file in MDCRD format. How about .nc?
        #info file names
        self.MININFO = self.RUN_PREF + '.' + conf.File_Naming.extMININFO
        self.HEATINFO = self.RUN_PREF + '.' + conf.File_Naming.extHEATINFO
        self.EQUIINFO = self.RUN_PREF + '.' + conf.File_Naming.extEQUIINFO
        self.MDINFO = self.RUN_PREF + '.' + conf.File_Naming.extMDINFO
        #logfile names
        self.MINLOG = self.RUN_PREF + '.' + conf.File_Naming.extMINLOG
        self.HEATLOG = self.RUN_PREF + '.' + conf.File_Naming.extHEATLOG
        self.EQUILOG = self.RUN_PREF + '.' + conf.File_Naming.extEQUILOG
        self.MDLOG = self.RUN_PREF + '.' + conf.File_Naming.extMDLOG
        #MD done text
        self.MD_DONE_TEXT = conf.MD_Defines.MD_GP_DONE_TEXT #Depending on solvation, this should change.Return later.
        #other parameters
        self.minimization_only = json_dict["minimization_only"]
        
    def CreateTLeapInputFile(self): #Creates a tLeap input file that creates minimization PARMTOP and RST7 files.
        pass

    def CreateMinimizationInputFile(self):
        min_in = open (self.WorkDir + '/' + self.MININ, 'w')
        min_in.write('Constant Volume Minimization\n')
        min_in.write(' # Control section\n')
        min_in.write(' &cntrl\n')
        min_in.write('  ntxo = 1,\n')
        min_in.write('  ntwx = 500, ntpr = 500,\n')
        min_in.write('  nsnb = 25, dielc = 80, cut = 12.0,\n')
        min_in.write('  ntb = 1,\n')
        min_in.write('  maxcyc = 10000, ntmin = 1, ncyc = 10000, dx0 = 0.01, drms = 0.0001,\n')
        min_in.write('  ntp = 0,\n')
        min_in.write('  ibelly = 0, ntr = 0,\n')
        min_in.write('  imin = 1,\n')
        min_in.write(' /\n')
        
    def CreateHeatingInputFile(self):
        heat_in = open (self.WorkDir + '/' + self.HEATIN, 'w')
        heat_in.write('Dynamic Simulation with Constant Volume\n')
        heat_in.write(' # Control section\n')
        heat_in.write(' &cntrl\n')
        heat_in.write('  ntwx = 500, ntpr = 500, iwrap=1,\n')
        heat_in.write('  ntt = 3, temp0 = 300.0, tempi = 5.0, tautp = 1.0,\n')
        heat_in.write('  dielc = 1, cut = 8.0, ig=3762986,\n')
        heat_in.write('  ntb = 1, ntc = 2, ntf = 2,\n')
        heat_in.write('  nstlim = 20000, dt = 0.0020,\n')
        heat_in.write('  ntp = 0, ibelly = 0, ntr = 0,\n')
        heat_in.write('  imin = 0, irest = 0, ntx = 1, nmropt = 1,\n')
        heat_in.write(' /\n')
        heat_in.write(' &wt\n')
        heat_in.write('  type = \'TEMP0\', istep1 = 1, istep2 = 20000, value1 = 5.0, value2 = 300.0,\n')
        heat_in.write(' /\n')
        heat_in.write(' &wt\n')
        heat_in.write('  type=\'END\'\n')
        heat_in.write(' /\n')
        heat_in.write('END\n')

    def CreateEquilibrationInputFile(self):
        equi_in = open(self.WorkDir + '/' + self.EQUIIN, 'w')
        equi_in.write('Dynamic Simulation with Constant Pressure(update ntwprt flag for each job)\n')
        equi_in.write(' # Control section\n')
        equi_in.write(' &cntrl\n')
        equi_in.write('  ntwx = 5000, ntpr = 1000, ntave = 5000,\n')
        equi_in.write('  ntt = 3, temp0 = 300.0, tempi = 300.0,\n')
        equi_in.write('  tautp = 1.0, gamma_ln=5.0,\n')
        equi_in.write('  dielc = 1, cut = 8.0, ig=3762986,\n')
        equi_in.write('  ntb = 2, ntc = 2, ntf = 2,\n')
        equi_in.write('  nstlim = 50000000, dt = 0.0020,\n')
        equi_in.write('  ntp = 1, taup = 2.0, comp = 44.6, pres0 = 1.0,\n')
        equi_in.write('  imin = 0, irest = 1, ntx = 5, iwrap=1, ioutfm=1,\n')
        equi_in.write(' /\n')

    def CreateProductionInputFile(self):
        equi_in = open(self.WorkDir + '/' + self.MDIN, 'w')
        equi_in.write('Dynamic Simulation with Constant Pressure(update ntwprt flag for each job)\n')
        equi_in.write(' # Control section\n')
        equi_in.write(' &cntrl\n')
        equi_in.write('  ntwx = 5000, ntpr = 1000, ntave = 5000,\n')
        #equi_in.write('  ntwprt = ' + self.ntwprt + '\n')
        equi_in.write('  ntt = 3, temp0 = 300.0, tempi = 300.0,\n')
        equi_in.write('  tautp = 1.0, gamma_ln=5.0,\n')
        equi_in.write('  dielc = 1, cut = 8.0, ig=3762986,\n')
        equi_in.write('  ntb = 2, ntc = 2, ntf = 2,\n')
        equi_in.write('  nstlim = 50000000, dt = 0.0020,\n')
        equi_in.write('  ntp = 1, taup = 2.0, comp = 44.6, pres0 = 1.0,\n')
        equi_in.write('  imin = 0, irest = 1, ntx = 5, iwrap=1, ioutfm=1,\n')
        equi_in.write(' /\n')

    def CreateSubmissionScript(self,json_dict):
        #Later determine MD command by another argument that reflect what settings are needed.
        self.MD_COMMAND='${AMBERHOME}/bin/sander'
        self.AMBERHOME = '/programs/amber16/'

        self.Run_Script_Name = '/' + self.RUN_PREF + '.sh'
        json_dict["sbatchArgument"] = "bash " + self.Run_Script_Name
        run_script = open(os.path.abspath(os.path.curdir) + self.Run_Script_Name, 'w')

        run_script.write("cd " + os.path.abspath(os.path.curdir) + "\n")
        run_script.write("export RUN_ID=\'" + self.JobId + "\'\n")
        run_script.write("export AMBERHOME=\'" + self.AMBERHOME + "\'\n")
        run_script.write("export MD_COMMAND=\'" + self.MD_COMMAND + "\'\n\n")
        run_script.write("# Initialize logging for this simulation\n")
        run_script.write("echo \"Beginning simulation run for webid ${RUN_ID} on $(date)\" >> ${LOGFILE}\n")
        run_script.write("# Record the nodes that will do the calculation\n")
        run_script.write("echo \"The minimization for webid ${RUN_ID} will run on these hosts:\" >> ${LOGFILE}\n")
        run_script.write("srun hostname -s | sort -u >slurm.hosts\n")
        run_script.write("cat slurm.hosts >> ${LOGFILE}\n")
        run_script.write("# Set up and run the simulation\n")
        run_script.write("source ${AMBERHOME}/amber.sh\n\n")
        run_script.write("# Do the minimization\n")
        run_script.write("\n")
        run_script.write("${MD_COMMAND} \\\n")
        run_script.write("  -p    " + self.PARMTOP + " \\\n")
        run_script.write("  -c    " + self.INPCRD + " \\\n")
        run_script.write("  -i    " + self.MININ + " \\\n")
        run_script.write("  -o    " + self.MINOUT +  " \\\n")
        run_script.write("  -r    " + self.MINRST + " \\\n")
        run_script.write("  -x    " + self.MINCRD + " \\\n")
        run_script.write("  -inf  " + self.MININFO + " \\\n\n")
        run_script.write("if grep -q \'" + self.MD_DONE_TEXT + "\' " + self.MINOUT + " ; then\n")
        run_script.write("    echo \"Minimization of webid ${RUN_ID} appears to be complete on $(date).\" >> ${LOGFILE}\n")
        run_script.write("else\n")
        run_script.write("    echo \"Minimization of webid ${RUN_ID} appears to have failed on $(date).Check " + self.MDOUT + "\" >> ${LOGFILE}\n")
        run_script.write("fi\n")

        if self.minimization_only != "Yes":
            run_script.write("${MD_COMMAND} \\\n")
            run_script.write("  -p    " + self.PARMTOP + " \\\n")
            run_script.write("  -c    " + self.MINRST + " \\\n")
            run_script.write("  -i    " + self.HEATIN + " \\\n")
            run_script.write("  -o    " + self.HEATOUT +  " \\\n")
            run_script.write("  -r    " + self.HEATRST + " \\\n")
            run_script.write("  -x    " + self.HEATCRD + " \\\n")
            run_script.write("  -inf  " + self.HEATINFO + " \\\n\n")
            run_script.write("if grep -q \'" + self.MD_DONE_TEXT + "\' " + self.HEATOUT + " ; then\n")
            run_script.write("    echo \"Heating of webid ${RUN_ID} appears to be complete on $(date).\" >> ${LOGFILE}\n")
            run_script.write("else\n")
            run_script.write("    echo \"Heating of webid ${RUN_ID} appears to have failed on $(date).Check " + self.MDOUT + "\" >> ${LOGFILE}\n")
            run_script.write("fi\n")

            run_script.write("${MD_COMMAND} \\\n")
            run_script.write("  -p    " + self.PARMTOP + " \\\n")
            run_script.write("  -c    " + self.HEATRST + " \\\n")
            run_script.write("  -i    " + self.EQUIIN + " \\\n")
            run_script.write("  -o    " + self.EQUIOUT +  " \\\n")
            run_script.write("  -r    " + self.EQUIRST + " \\\n")
            run_script.write("  -x    " + self.EQUICRD + " \\\n")
            run_script.write("  -inf  " + self.EQUIINFO + " \\\n\n")
            run_script.write("if grep -q \'" + self.MD_DONE_TEXT + "\' " + self.EQUIOUT + " ; then\n")
            run_script.write("    echo \"Equilibration of webid ${RUN_ID} appears to be complete on $(date).\" >> ${LOGFILE}\n")
            run_script.write("else\n")
            run_script.write("    echo \"Equilibration of webid ${RUN_ID} appears to have failed on $(date).Check " + self.MDOUT + "\" >> ${LOGFILE}\n")
            run_script.write("fi\n")

            run_script.write("${MD_COMMAND} \\\n")
            run_script.write("  -p    " + self.PARMTOP + " \\\n")
            run_script.write("  -c    " + self.EQUIRST + " \\\n")
            run_script.write("  -i    " + self.MDIN + " \\\n")
            run_script.write("  -o    " + self.MDOUT +  " \\\n")
            run_script.write("  -r    " + self.MDRST + " \\\n")
            run_script.write("  -x    " + self.MDCRD + " \\\n")
            run_script.write("  -inf  " + self.MDINFO + " \\\n\n")
            run_script.write("if grep -q \'" + self.MD_DONE_TEXT + "\' " + self.EQUIOUT + " ; then\n")
            run_script.write("    echo \"MD simulation of webid ${RUN_ID} appears to be complete on $(date).\" >> ${LOGFILE}\n")
            run_script.write("else\n")
            run_script.write("    echo \"MD simulation of webid ${RUN_ID} appears to have failed on $(date).Check " + self.MDOUT + "\" >> ${LOGFILE}\n")
            run_script.write("fi\n")

        run_script.close()

    def check_if_dir_content_good(self, logFile):
        #Previous function should cd into working directory.So file path is omitted in this function. 
        input_files_missing = False
        out_files_exist = False
        if os.path.isfile(self.WorkDir + "/" + self.PARMTOP) == False:
            input_files_missing = True
            print('Parmtop file missing in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.INPCRD) == False:
            input_file_missing = True
            print('Inpcrd file missing in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MININ) == False:
            input_file_missing = True
            print('MININ file missing in sub directory %s'%(os.path.abspath(os.path.curdir)))

        if self.minimization_only != "Yes":
            if os.path.isfile(self.WorkDir + "/" + self.HEATIN) == False:
                input_file_missing = True
                print('HEATIN file missing')
            if os.path.isfile(self.WorkDir + "/" + self.EQUIIN) == False:
                input_file_missing = True
                print('EQUIIN file missing')
            if os.path.isfile(self.WorkDir + "/" + self.MDIN)  == False:
                input_file_missing = True
                print('MDIN file missing')

        if input_files_missing == True:
            logFile.write('Error, one or more input files are missing in working directory: %s\n'%(os.path.abspath(os.path.curdir)) )
            return False

        if os.path.isfile(self.WorkDir + "/" + self.MINOUT) == True:
            out_files_exist = True
            print('MDOUT file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MINCRD) == True:
            out_files_exist = True
            print('MDCRD file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MININFO) == True:
            out_files_exist = True
            print('MDINFO file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MINLOG) == True:
            out_files_exist = True
            print('MINLOG file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MINRST) == True:
            out_files_exist = True
            print('MINRST file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))


        if out_files_exist == True:
            logFile.write('Error, one or more output files already exist in working directory: %s\n'%(os.path.abspath(os.path.curdir)))
            return False

        elif input_files_missing == False and out_files_exist == False:
            return True

if __name__ == "__main__":
    import os,sys,json
    input_json_dict = {}
    with open('input.json') as input_json:
        input_json_dict = json.load(input_json)
    logFile = open('amber.log', 'w')
    amber_job = Amber_Job(input_json_dict)
    if input_json_dict['minimization_only'] == 'Yes':
        amber_job.CreateMinimizationInputFile()
        amber_job.CreateSubmissionScript(json_dict)
    else:
        amber_job.CreateMinimizationInputFile()
        amber_job.CreateHeatingInputFile()
        amber_job.CreateEquilibrationInputFile()
        amber_job.CreateProductionInputFile()
        amber_job.CreateSubmissionScript(input_json_dict)

    if amber_job.check_if_dir_content_good(logFile) == False:
        slurm_module_path = '../../batchcompute' 
        sys.path.append(os.path.abspath(slurm_module_path))
        print("Importing path: " + os.path.abspath(slurm_module_path))
        import slurm.receive.main as slurm_receive
        outgoing_json_dict = {}
        #"partition"        : "amber",
        #"user"             : "webdev",
        #"name"             : "testMin",
        #"workingDirectory" : "/website/TESTS/build-minimize",
        #"sbatchArgument"   : "run.bash"
        outgoing_json_dict["partition"] = input_json_dict["queue_partition"]
        outgoing_json_dict["user"] = input_json_dict["user"]
        outgoing_json_dict["name"] = input_json_dict["name"]
        outgoing_json_dict["workingDirectory"] = input_json_dict["workingDirectory"]
        outgoing_json_dict["sbatchArgument"] = "bash " + amber_job.Run_Script_Name 
        
        slurm_receive(outgoing_json_dict)

    logFile.close()
