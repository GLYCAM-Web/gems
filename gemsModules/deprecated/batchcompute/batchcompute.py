#!/usr/bin/python3.9

import sys
import os
import json
import subprocess 

def batch_compute_delegation (incoming_json_dict):
    #For right now, slurm in the only agent for batch compute to call.
    from gemsModules.deprecated.batchcompute.slurm import receive as slurm_receive
    print("1")
    slurm_basic_submission_json = {}
    print("2")
    workdir = incoming_json_dict["workingDirectory"]
    print("3")
    sbatch_argument = incoming_json_dict["sbatchArgument"]
    
    print("4")
    minimal_json_dict = incoming_json_dict
    print("5")
    output_str = json.dumps(minimal_json_dict)
    print("6")
    slurm_receive.manageIncomingString(output_str)
    print("7")
#    slurm_receive.manageIncomingString(json.dumps(incoming_json_dict))

    
if (__name__ == '__main__'):
    batch_compute (sys.argv[1])

  
