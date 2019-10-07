#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='Sequence'

## Module names for services that this entity/module can perform.
serviceModules = {
    'Validate' : 'validate',
    'Evaluate' : 'evaluate',
    'Build3DStructure' : 'build3Dstructure'
}

