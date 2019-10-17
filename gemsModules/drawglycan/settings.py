#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='DrawGlycan'

## Module names for services that this entity/module can perform.
serviceModules = {
    'Draw' : 'draw',
}

