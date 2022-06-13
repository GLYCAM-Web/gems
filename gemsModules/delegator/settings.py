#!/usr/bin/env python3
import traceback
from enum import Enum
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


WhoIAm='Delegator'

# Names of available services in JSON mapped to internal names
class AvailableServices(str, Enum) :
    delegate     = 'Delegate'
    listEntities = 'ListEntities'
    marco        = 'Marco'

    @classmethod
    def get_list(self):
        theList = []
        for item in self :
            theList.append(item.value)
        return theList


## List of entities that the Delegator knows about
class KnownEntities(str, Enum) :
    batchcompute  = 'BatchCompute'
    drawglycan    = 'DrawGlycan'
    glycomimetic  = 'Glycomimetic'   
    glycoprotein  = 'Glycoprotein'   
    mmservice     = 'MmService'      
    query         = 'Query'          
    sequence      = 'Sequence'       
    status        = 'Status'         
    structureFile = 'StructureFile'  

    @classmethod
    def get_list(self):
        theList = []
        for item in self :
            theList.append(item.value)
        return theList

## Module location for entities that the Delegator knows about
class subEntities(str, Enum) :
    BatchCompute   = 'batchcompute'
    Delegator      = 'delegator'
    DrawGlycan     = 'drawglycan'
    Glycomimetic   = 'complex/glycoprotein'
    Glycoprotein   = 'conjugate/glycoprotein'
    MmService      = 'mmservice'
    Query          = 'query'
    Sequence       = 'sequence'
    Status         = 'status'
    StructureFile  = 'structureFile'

    @classmethod
    def get_list(self):
        theList = []
        for item in self :
            theList.append(item.value)
        return theList

if __name__ == "__main__":
    print("This is my name:  " + str(WhoIAm))
    print("The entities known to me are: ")
    print(KnownEntities.get_list())
    print("My available services are: ")
    print(AvailableServices.get_list())

    print("here is a subEntity entry")
    theEntity='Delegator'
    print(subEntities[theEntity].value)
    print("here is a subEntity entry again")
    print(subEntities['Delegator'].value)

