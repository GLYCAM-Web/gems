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
  print("Creating a file and checking that it exists.")
  CreateLogFile(filename)
  assert filepath.is_file(), "File should exist, but appears not to."

  print("Appending a line to the file and checking file contents.")
  appendstring="Hello, world!  I'm a log file!"
  AppendLogFile(filename,appendstring)
  with open(filename, 'r') as f:
    contents=(f.read())
    assert contents == appendstring , "File content is not correct."
 
  print("Deleting the file and checking that it is gone.")
  RemoveLogFile(filename)
  print("  Checking to see if that file exists.")
  assert filepath.is_file() == False , "File should not be present, but is."
 
