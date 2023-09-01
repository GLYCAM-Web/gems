#!/usr/bin/env python3
import traceback
import os, sys, subprocess, signal


from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def slurm_submit(thisSlurmJobInfo):
    response = run_slurm_submission_script(thisSlurmJobInfo)
    if response is None:
        log.error("Got none response")
        # TODO: return a proper error response.
    else:
        thisSlurmJobInfo.copyJobinfoInToOut()
        thisSlurmJobInfo.addSbatchResponseToJobinfoOut(response)
        log.debug("The outgoing dictionary is: \n")
        log.debug(str(thisSlurmJobInfo.outgoing_dict))
        log.debug("\n")

        return thisSlurmJobInfo.outgoing_dict


# TODO: TO a task?
def run_slurm_submission_script(thisSlurmJobInfo):
    log.debug("run_slurm_submission_script() was called.\n")

    if "sbatchArgument" not in thisSlurmJobInfo.incoming_dict.keys():
        return "SLURM submit cannot find sbatch submission arguments."

    if thisSlurmJobInfo.incoming_dict["workingDirectory"] is not None:
        try:
            os.chdir(thisSlurmJobInfo.incoming_dict["workingDirectory"])
        except Exception as error:
            log.error("Was unable to change to the working directory.")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())
            return "Was unable to change to the working directory."
    log.debug("The current directory is:  " + os.getcwd())
    try:
        log.debug(
            "In func run_slurm_submission_script, incoming dict sbatchArg is: "
            + thisSlurmJobInfo.incoming_dict["sbatchArgument"]
            + "\n"
        )
        p = subprocess.Popen(
            ["sbatch", thisSlurmJobInfo.incoming_dict["slurm_runscript_name"]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (outputhere, errorshere) = p.communicate()
        if p.returncode != 0:
            return "SLURM submit got non-zero exit upon attempt to submit."
        else:
            log.debug("outputhere in raw form: " + str(outputhere))
            theOutput = outputhere.decode("utf-8")
            log.debug("outputhere stripped: " + theOutput)
            return theOutput
    except Exception as error:
        log.error("Was unable to submit the job.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        return "Was unable to submit the job."
