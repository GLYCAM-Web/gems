import re
import os


from file_type import is_PDB

os.chdir("pdb_tests")

files = os.listdir()

for file in files:
    if os.path.isfile(file):
        print(file)
        print(is_PDB(file) + "\n")
    else:
        print(file)
        print("This is a folder\n")