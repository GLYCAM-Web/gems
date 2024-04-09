# Standard python libraries
import os 
import json
import magic

# My module
from mime_type import get_mime_type

""" 
This script requires that you have made a D-Mannose build, which has a sequence folder in the user data folder.
First, let's generate a text file containing the output file names, sizes, and MIME types for an unreasonably small mannose build called "tenth_of_a_mannose.txt"
"""
# Change to the sequence's directory

for seq in os.listdir("/home/sam/Desktop/GLYCAM_Dev_Env/V_2/Web_Data/userdata/sequence/cb/Sequences"):

    # Change to the current sequences' directory
    
    with open(f"/home/sam/Desktop/GLYCAM_Dev_Env/V_2/Web_Data/userdata/sequence/cb/Sequences/{seq}/evaluation.json") as f:
        data = json.load(f)


    if data["entity"]["inputs"]["sequence"]["payload"] == "DManpa1-OH":

        os.chdir(f"/home/sam/Desktop/GLYCAM_Dev_Env/V_2/Web_Data/userdata/sequence/cb/Sequences/{seq}/buildStrategyID1/All_Builds/structure")

        curr_dict = {}

        outputs = os.listdir()

        # Make lists for non-slurm files and their file sizes
        for file in outputs:
            if "slurm" in file:
                pass
            else:
                # calculate file size
                props = os.stat(file)

                # add file to a dictionary with file size and MIME
                curr_dict[file] = [int(props.st_size/10), get_mime_type(file)]

        

        # Now write the contents of the dictionary to the file "tenth_of_mannose.txt"

        with open('/home/sam/Desktop/GLYCAM_Dev_Env/V_2/Web_Programs/gems/daily_build_checker/tenth_of_mannose.txt', 'w') as f:
            f.write(f"{'File': <60}{'Size (Bytes)' : ^20}{'Type' : >30}")
            f.write("\n")
        
            for file in curr_dict.keys():

                f.write(f"{file: <60}{curr_dict[file][0]: ^20}{curr_dict[file][1] : >30}")
                f.write("\n")

        