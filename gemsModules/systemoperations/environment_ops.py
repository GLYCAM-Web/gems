#!/usr/bin/env python3
import os, sys
import importlib

from gemsModules.common.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def get_gems_path() -> str :
    return os.environ.get('GEMSHOME')

def gemsModules_is_findable() -> bool :
    if importlib.util.find_spec("gemsModules") is None :
        return True
    else :
        return False

def add_gems_to_python_path() -> None :
    GemsPath = get_gems_path()
    sys.path.append(GemsPath)


# def check_gems_home() -> int:
## This probably isn't used and probably should not be used
## It is an old function that tried to be overly kind to users


