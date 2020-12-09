#!/usr/bin/env python3
##
## This file generates the command-line info for a file
##
import os, sys
from gemsModules.common.loggingConfig import *
from gemsModules.common.loggingConfig import *
from . import conf

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

class Amber_MD_Run_Control:
    def __init__(self, json_dict):
        #Environment settings
        #Later determine MD command by another argument that reflect what settings are needed.
        self.AMBERHOME = '/programs/amber'
        self.MD_COMMAND = 'sander' #Later determine this based on input json file. For now, just sander
        self.RUN_LOG = 'run.log'
        self.RUN_PREF = conf.File_Naming.prefSTRUCTURE
#        self.RUN_PREF = conf.File_Naming.prefSTRUCTURE + conf.File_Naming.modION + conf.File_Naming.modSOLV
        self.Run_Script_Name = self.RUN_PREF + '.bash'
	#Job id
        self.JobId = str (json_dict["project"]["id"])
        self.WorkDir = str (json_dict["project"]["workingDirectory"])
        #Expect the 1st member of that list to be prmtop name, the 2nd to be teh inpcrd name
#        self.PARMTOP = str (json_dict["project"]["prmtop_file_name"])
#        self.INPCRD = str (json_dict["project"]["inpcrd_file_name"])
        self.PARMTOP =  self.RUN_PREF + '.' +  conf.File_Naming.extPARM
        self.INPCRD =  self.RUN_PREF + '.' +  conf.File_Naming.extINPCRD
        log.debug ("self PARMTOP is " + self.PARMTOP )
        log.debug ("self INPCRD is " + self.INPCRD )
        #input file names
        self.LEAPIN = self.RUN_PREF + '.' + conf.File_Naming.extLEAPIN
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
        #PDB file names
        self.MINPDB = self.RUN_PREF + '_min.' + conf.File_Naming.extPDB 
        #logfile names
        self.MINLOG = self.RUN_PREF + '.' + conf.File_Naming.extMINLOG
        self.HEATLOG = self.RUN_PREF + '.' + conf.File_Naming.extHEATLOG
        self.EQUILOG = self.RUN_PREF + '.' + conf.File_Naming.extEQUILOG
        self.MDLOG = self.RUN_PREF + '.' + conf.File_Naming.extMDLOG
        #MD done text
        self.MD_DONE_TEXT = conf.MD_Defines.MD_GP_DONE_TEXT #Depending on solvation, this should change.Return later.
        #other parameters
        if json_dict["project"]["type"] == "minimization":
            self.minimization_only = True;
            self.CreateTLeapInputFile()
            self.CreateMinimizationInputFile()
            self.CreateSubmissionScript(json_dict)
        else:
            self.minimization_only = False;
            self.CreateTLeapInputFile()
            self.CreateMinimizationInputFile()
            self.CreateHeatingInputFile()
            self.CreateEquilibrationInputFile()
            self.CreateProductionInputFile()
            self.CreateSubmissionScript(input_json_dict)

        self.phase = json_dict["project"]["system_phase"] #gas or solvent
        self.water_model = json_dict["project"]["water_model"] #tip 3p/4p/5p or none (gas phase)

    def CreateTLeapInputFile(self): #Creates a tLeap input file that creates minimization PARMTOP and RST7 files.
        tleap_in = open (self.WorkDir + '/' + self.LEAPIN, 'w')
        log.debug("Attempting to open this file as tleap in >>>" + self.WorkDir + '/' + self.LEAPIN + "<<<")
        tleap_in.write('verbosity 0\n')
        tleap_in.write('logfile leap.log\n')
        tleap_in.write('source leaprc.GLYCAM_06j-1 \n')
        tleap_in.write('loadoff structure.off \n')
        tleap_in.write('check CONDENSEDSEQUENCE \n')
        tleap_in.write('saveamberparm CONDENSEDSEQUENCE ' + self.PARMTOP + ' ' + self.INPCRD + '\n')
        tleap_in.write('quit\n')

    def CreateMinimizationInputFile(self):
        min_in = open (self.WorkDir + '/' + self.MININ, 'w')
        min_in.write('Gas Phase Minimization\n')
        min_in.write(' &cntrl\n')
        min_in.write('  imin = 1, maxcyc = 10000, ncyc = 5000, dt = 0.001 ,\n')
        min_in.write('  ntb = 0, cut = 20.0, ntmin = 1, nscm = 100, dielc = 1 ,\n')
        min_in.write('  ntxo = 1, ntwr = 1,\n')
        min_in.write(' &end \n')

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
        run_script = open(os.path.abspath(self.WorkDir + "/" + self.Run_Script_Name), 'w')
        run_script.write("#!/bin/bash\n")
        run_script.write("export LOGFILE=\'" + self.RUN_LOG + "\'\n\n")
        run_script.write("echo \"Run log begin on $(date) \" > ${LOGFILE}"  + "\n")
        run_script.write("export AMBERHOME=" + self.AMBERHOME + "\n")
        run_script.write("echo \"Sourcing amber.sh \" > ${LOGFILE}" + "\n")
        run_script.write("source ${AMBERHOME}/amber.sh\n")


        #For now don't call tleap to make Prmtop and rst7, they are provided by the user. The create tleap input file function is currently empty
        run_script.write("echo \"Running tleap...\" >> ${LOGFILE}" + "\n")
        run_script.write("tleap -f " + self.LEAPIN + "\n")


        run_script.write("echo \"Running sander...\" >> ${LOGFILE}" + "\n")
        run_script.write("\n")
        run_script.write("cd " + self.WorkDir + "\n")
        run_script.write("export RUN_ID=\'" + self.JobId + "\'\n")
        run_script.write("export AMBERHOME=\'" + self.AMBERHOME + "\'\n")
        run_script.write("export MD_COMMAND=\'" + self.MD_COMMAND + "\'\n\n")
        run_script.write("echo \"Beginning simulation run for webid ${RUN_ID} on $(date)\" > ${LOGFILE}\n")
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
        run_script.write("    ambpdb -p " + self.PARMTOP + " -c " + self.INPCRD + " > " + self.MINPDB + " 2> " + "ambpdb" + ".stderr\n")
        run_script.write("else\n")
        run_script.write("    echo \"Minimization of webid ${RUN_ID} appears to have failed on $(date).Check " + self.MINOUT + "\" >> ${LOGFILE}\n")
        run_script.write("    exit 1\n")
        run_script.write("fi\n")


        if self.minimization_only != True:
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
            run_script.write("    echo \"Heating of webid ${RUN_ID} appears to have failed on $(date).Check " + self.HEATOUT + "\" >> ${LOGFILE}\n")
            run_script.write("    exit 1\n")
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
            run_script.write("    echo \"Equilibration of webid ${RUN_ID} appears to have failed on $(date).Check " + self.EQUIOUT + "\" >> ${LOGFILE}\n")
            run_script.write("    exit 1\n")
            run_script.write("fi\n")

            run_script.write("${MD_COMMAND} \\\n")
            run_script.write("  -p    " + self.PARMTOP + " \\\n")
            run_script.write("  -c    " + self.EQUIRST + " \\\n")
            run_script.write("  -i    " + self.MDIN + " \\\n")
            run_script.write("  -o    " + self.MDOUT +  " \\\n")
            run_script.write("  -r    " + self.MDRST + " \\\n")
            run_script.write("  -x    " + self.MDCRD + " \\\n")
            run_script.write("  -inf  " + self.MDINFO + " \\\n\n")
            run_script.write("if grep -q \'" + self.MD_DONE_TEXT + "\' " + self.MDOUT + " ; then\n")
            run_script.write("    echo \"MD simulation of webid ${RUN_ID} appears to be complete on $(date).\" >> ${LOGFILE}\n")
            run_script.write("else\n")
            run_script.write("    echo \"MD simulation of webid ${RUN_ID} appears to have failed on $(date).Check " + self.MDOUT + "\" >> ${LOGFILE}\n")
            run_script.write("    exit 1\n")
            run_script.write("fi\n")

        run_script.close()

    def check_if_dir_content_good(self):
        #Previous function should cd into working directory.So file path is omitted in this function.
        input_files_missing = False
        out_files_exist = False
#        if os.path.isfile(self.WorkDir + "/" + self.PARMTOP) == False:
#            input_files_missing = True
#            log.debug('Parmtop file missing in sub directory %s'%(os.path.abspath(self.WorkDir)))
#        if os.path.isfile(self.WorkDir + "/" + self.INPCRD) == False:
#            log.debug ("Test:" + self.WorkDir + "/" + self.INPCRD)
#            input_file_missing = True
#            log.debug('Inpcrd file missing in sub directory %s'%(os.path.abspath(self.WorkDir)))
        if os.path.isfile(self.WorkDir + "/" + self.MININ) == False:
            input_file_missing = True
            log.debug('MININ file missing in sub directory %s'%(os.path.abspath(self.WorkDir)))

        if self.minimization_only != True:
            if os.path.isfile(self.WorkDir + "/" + self.HEATIN) == False:
                input_file_missing = True
                log.debug('HEATIN file missing')
            if os.path.isfile(self.WorkDir + "/" + self.EQUIIN) == False:
                input_file_missing = True
                log.debug('EQUIIN file missing')
            if os.path.isfile(self.WorkDir + "/" + self.MDIN)  == False:
                input_file_missing = True
                log.debug('MDIN file missing')

        if input_files_missing == True:
            return False

        if os.path.isfile(self.WorkDir + "/" + self.MINOUT) == True:
            out_files_exist = True
            log.debug('MDOUT file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MINCRD) == True:
            out_files_exist = True
            log.debug('MDCRD file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MININFO) == True:
            out_files_exist = True
            log.debug('MDINFO file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MINLOG) == True:
            out_files_exist = True
            log.debug('MINLOG file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))
        if os.path.isfile(self.WorkDir + "/" + self.MINRST) == True:
            out_files_exist = True
            log.debug('MINRST file already exists in sub directory %s'%(os.path.abspath(os.path.curdir)))


        if out_files_exist == True:
            return False

        elif input_files_missing == False and out_files_exist == False:
            return True


def manageIncomingString(jsonObjectString: str):
    import os,sys,json
#    input_json_dict = {}
    input_json_dict = json.loads(jsonObjectString)

    amber_job = Amber_Job(input_json_dict)

    if amber_job.check_if_dir_content_good() == True:
        from gemsModules.batchcompute import batchcompute
        slurm_module_path = '../../batchcompute'
        sys.path.append(os.path.abspath(slurm_module_path))
        outgoing_json_dict = {}
        outgoing_json_dict["partition"] = "amber"
        outgoing_json_dict["user"] = "webdev"
        outgoing_json_dict["name"] = "testmin"
        outgoing_json_dict["workingDirectory"] = str(input_json_dict["project"]["workingDirectory"])
        outgoing_json_dict["sbatchArgument"] = amber_job.Run_Script_Name

        batchcompute.batch_compute_delegation(outgoing_json_dict)

def main():
    import importlib.util, os, sys
    #from importlib import util
    if importlib.util.find_spec("gemsModules") is None:
        this_dir, this_filename = os.path.split(__file__)
        sys.path.append(this_dir + "/../")
        if importlib.util.find_spec("common") is None:
            print("I cannot find the Common Servicer.  No clue what to do. Exiting")
            sys.exit(1)
        else:
            from common import utils
    else:
        from gemsModules.common import utils
    jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
    try:
        responseObject=manageIncomingString(jsonObjectString)
    except Exception as error:
        print("\nThe mmservice.amber module captured an error.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())
        ##TODO: see about exploring this error and returning more info. Temp solution for now.
        responseObject = {
            'response' : {
                'type' : 'UnknownError',
                'notice' : {
                    'code' : '500',
                    'brief' : 'unknownError',
                    'blockID' : 'unknown',
                    'message' : 'Not sure what went wrong. Error captured by the mmservice.amber gemsModule.'
                }
            }
        }
        responseObjectString = str(responseObject)


    print("\nmmservice.amber is returning this: \n" +  responseObjectString)


if __name__ == "__main__":
    main()

