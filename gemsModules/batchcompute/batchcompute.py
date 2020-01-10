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
    with open(workdir + "/" + "basic_submission.json", "w") as slurm_basic_json: 
        json.dump(minimal_json_dict, slurm_basic_json)         

    json_path = workdir + "/" + "basic_submission.json"
    print ("/programs/gems/bin/slurmreceive " + json_path)
    try:
        p = subprocess.Popen( [ "/programs/gems/bin/slurmreceive ", json_path] ,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        print ("Stdout is:" + str(out) + "\n")
        print ("Stderr is:" + str(err) + "\n")
    except Exception as error:
        print("Was unable to call /programs/gems/bin/slurmreceive\n")
        print(error.message)

    
if (__name__ == '__main__'):
    batch_compute (sys.argv[1])

  
