import sys, os, re, importlib.util
import gemsModules
import gmml
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
from . import settings

def receive(thisTransaction : Transaction):
    print("status gemsModule receive.py receive() was called.")

    if not 'services' in thisTransaction.request_dict['entity'].keys():
        print("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return

def doDefaultService(thisTransaction : Transaction):
    print("doDefaultService() was called.")

def main():
    pass

if __name__ == "__main__":
  main()
