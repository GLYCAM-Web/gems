#!/usr/bin/env python3
from gemsModules import common
from gemsModules.common.transaction import *
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema

## Who I am
WhoIAm='Sequence'

## Module names for services that this entity/module can perform.
serviceModules = {
        'Marco' : 'common.services.marco',
        'ListEntities' : 'common.services.listEntities',
        'ReturnHelp' : 'common.services.returnHelp',
        'ReturnUsage' : 'common.services.returnHelp',
        'ReturnVerboseHelp' : 'common.services.returnHelp',
        'ReturnSchema' : 'common.services.returnHelp'
        'Evaluate' : 'sequence.entity.evaluate'
        'Build3DStructure' : 'sequence.entity.build3Dstructure'
        }

