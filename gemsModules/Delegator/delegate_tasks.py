#!/usr/bin/env python3
import sys
import os
import subprocess
import json
from io import StringIO

class delegatedTask(object):

  def __init__(self, jsonObject):
    self.__dict__ = json.loads(jsonObject)

  def assign


def delegate_task():
  

def delegate_task(jsonObject):
  
  file=sys.stdout 

def delegate_task(jsonObject,logPath=sys.stdout):




if (__name__ == '__main__'):
  import sys
  import os

  # check the command line
  if len(sys.argv) != 1:
      print('Must supply exactly 1 argument, and that argument must be the name of a file containing a JSON object.')
      print('%d arguments are supplied'%(len(sys.argv)-1) )
      sys.exit()

  # check out the environment
  GemsPath = os.environ.get('GEMSHOME')
  if GemsPath == None:
      print("""

Must set GEMSHOME environment variable

    BASH:  export GEMSHOME=/path/to/gems
    SH:    setenv GEMSHOME /path/to/gems

""")
      sys.exit(1)

  if os.path.isfile(sys.argv[1]) == False:
      print('Argument 1: "' + sys.argv[1] + '" is not a file')
      sys.exit()

## fix me....
##  batch_compute ( sys.argv[1], sys.argv[2] )

