import os
def CreateLogFile(file_path):
    logFile = open(file_path,"w+")
    logFile.close()

def RemoveLogFile(file_path):
    os.remove(file_path)

def AppendLogFile(file_path, line_content):
    logFile = open(file_path, "a")
    logFile.write(line_content)
    logFile.close()


