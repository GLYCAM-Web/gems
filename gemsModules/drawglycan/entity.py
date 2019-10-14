import sys, os, re, importlib.util
import gemsModules
import gmml

from . import settings
from gemsModules.common.services import *
from gemsModules.common.transaction import *


def receive(thisTransaction : Transaction):
    print("~~~DrawGlycan entity has received a transation.")
