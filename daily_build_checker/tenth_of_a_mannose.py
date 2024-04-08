import os 
from mime_type import mime_type

""" 
First, let's just go into the first sequence's folder and print out all the non-slurm output files and their file sizes.
"""
# Change to the sequence's directory

os.chdir("/home/sam/Dropbox/cb/Sequences/866ded1c-252e-5b3f-8264-32ab9a845628/buildStrategyID1/All_Builds/structure")

outputs = os.listdir()

files = []
sizes = []
types = []


# Make lists for non-slurm files and their file sizes
for file in outputs:
    if "slurm" in file:
        pass
    else:
        files.append(file)

        props = os.stat(file)
        sizes.append(int(props.st_size/10))

        types.append(mime_type(file))

        

 # Now just take the first file in the list and assume those are the expected outputs and write them to a file




#aligned_text_file = open("single_seq_aligned.txt", "w")

#with open("single_seq.txt")
        



with open('/home/sam/Dropbox/cb/tenth_of_a_mannose.txt', 'w') as f:
    f.write(f"{'File': <60}{'Size (Bytes)' : ^20}{'Type' : >30}")
    f.write("\n")
   
    for file, size, type in zip(files, sizes, types):

        f.write(f"{file : <60}{size: ^20}{type : >30}")
        f.write("\n")

## You tried to write out bolded text, but it turns out ".txt" files do not support any other formats (different fontsize, bold, italics, etc.)