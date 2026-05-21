from gemsmodules.systemoperations.filesystem_ops import file_ops

def writeSlurmSubmissionScript(path, thisSlurmJobInfo):
    import sys, os
    try:
        script = open(path, "w")
    except Exception as error:
        log.error("Cannnot write slurm run script. Aborting")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        raise error
        #sys.exit(1)

    incoming_dict = thisSlurmJobInfo.incoming_dict

    GEMS_MD_TEST_WORKFLOW = 'False'
    try :
        GEMS_MD_TEST_WORKFLOW = os.environ.get('GEMS_MD_TEST_WORKFLOW')
        log.debug("got GEMS_MD_TEST_WORKFLOW and it is:  " + str(GEMS_MD_TEST_WORKFLOW) )
    except Exception as error :
        log.error("Cannnot determine workflow status.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())

    script.write("#!/bin/bash" + "\n")
    script.write("#SBATCH --chdir=" + incoming_dict["workingDirectory"] + "\n")
    script.write("#SBATCH --error=slurm_%x-%A.err" + "\n")
    script.write("#SBATCH --get-user-env" + "\n")
    script.write("#SBATCH --job-name=" + incoming_dict["name"] + "\n")
    script.write("#SBATCH --nodes=1" + "\n")
    script.write("#SBATCH --output=slurm_%x-%A.out" + "\n")
    script.write("#SBATCH --partition=" + incoming_dict["partition"] + "\n")
    script.write("#SBATCH --tasks-per-node=4" + "\n")
#  The following was needed until Slurm did their security fix.
#  Something like it might be needed by someone one day.
#    script.write("#SBATCH --uid=" + incoming_dict["user"] + "\n")
    script.write("\n")
    log.debug("still have GEMS_MD_TEST_WORKFLOW and it is:  " + str(GEMS_MD_TEST_WORKFLOW) )
    if GEMS_MD_TEST_WORKFLOW == 'True' :
        log.debug("setting testing workflow to yes")
        script.write("export MDUtilsTestRunWorkflow=Yes" + "\n")
        script.write("\n")
    else :
        log.debug("NOT setting testing workflow to yes")
    log.debug("The sbatchArgument is : " + incoming_dict["sbatchArgument"])
    script.write(incoming_dict["sbatchArgument"] + "\n")

