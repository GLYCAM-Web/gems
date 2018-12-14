import os
from pathlib import Path
def CreateLogFile(file_path):
    logFile = open(file_path,"w+")
    logFile.close()

def RemoveLogFile(file_path):
    os.remove(file_path)

def AppendLogFile(file_path, line_content):
    logFile = open(file_path, "a")
    logFile.write(line_content)
    logFile.close()

if (__name__ == '__main__'):
  filename="log.dum"
  filepath=Path(filename)
  print("""
Creating a file called >>>""" + filename + "<<< in the current directory.")
  CreateLogFile(filename)
  print("  Checking to see if that file exists.")
  if filepath.is_file() :
    print("    File exists")
  else:
    print("    File does not exist.  Exiting now because nothing else to do")
    sys.exit()
 
  appendstring="Hello, world!  I'm a log file!"
  print("""
Appending this line:  
  >>>""" + appendstring + """<<<
  to the file.""")
  AppendLogFile(filename,appendstring)
  print("""
Here is the content of that file.
++++++++++++++++++++++++++++++++++++++++++""")
  with open(filename, 'r') as f:
    print(f.read())
  print("""++++++++++++++++++++++++++++++++++++++++++
If the contents aren't as expected, then something is wrong.""")
 
  print("""
Deleting the file called >>>""" + filename + "<<< in the current directory.")
  RemoveLogFile(filename)
  print("  Checking to see if that file exists.")
  if filepath.is_file() :
    print("    File exists!  There is a problem!  Please fix it, and remove the file.")
  else:
    print("    File no longer exists.  All is well!")
 
