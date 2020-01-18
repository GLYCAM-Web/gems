#!/usr/bin/python3.4

import sys
import os
import json
import subprocess 

def batch_compute_delegation (incoming_json_dict):
    #For right now, slurm in the only agent for batch compute to call.
    import slurm.receive as slurm_receive
    slurm_basic_submission_json = {}
    workdir = incoming_json_dict["workingDirectory"]
    sbatch_argument = incoming_json_dict["sbatchArgument"]
    
    minimal_json_dict = incoming_json_dict
    output_str = json.dumps(minimal_json_dict)
    slurm_receive.manageIncomingString(output_str)

    
if (__name__ == '__main__'):
    batch_compute (sys.argv[1])

  
