#!/usr/bin/env python3
import subprocess 
#from subprocess import *
import signal

def handler(signum,frame):
    print "Error Occured",signum
    raise IOError("Segmentation Fault Occured.")

#The C++ code is already compiled

#a = subprocess.Popen(["./isegfault"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
a = subprocess.Popen(["./isegfault"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(outputhere,errorshere) = a.communicate()
print("The output is: " + outputhere)
print("The error is: " + errorshere)
print("The return code is:  " )
print(a.returncode )
if a.returncode == -11 or a.returncode == 139:
    print("You got a segfault!")

try:
    signal.signal(signal.SIGSEGV,handler)  
    signal.signal(signal.SIGCHLD,handler)  
    print("The output is: " + outputhere)
    print("The error is: " + errorshere)
except IOError as e:
    print e
    print("The output is: " + outputhere)
    print("The error is: " + errorshere)
