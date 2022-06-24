#!/usr/bin/env python3
import traceback
from gemsModules.common.loggingConfig import *
from gemsModules.common.utils import GemsStrEnum

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

WhoIAm='Delegator'

# Names of available services in JSON mapped to internal names
class AvailableServices(GemsStrEnum) :
    delegate     = 'Delegate'
    listEntities = 'ListEntities'
    marco        = 'Marco'

## List of entities that the Delegator knows about
#  Please compare to subEntities 
#  For Pydantic, it needs to be in this key:value order
#  If you can merge these, please do so.
class KnownEntities(GemsStrEnum) :
    batchcompute  = 'BatchCompute'
    drawglycan    = 'DrawGlycan'
    glycomimetic  = 'Glycomimetic'   
    glycoprotein  = 'Glycoprotein'   
    mmservice     = 'MmService'      
    query         = 'Query'          
    sequence      = 'Sequence'       
    status        = 'Status'         
    structureFile = 'StructureFile'  

## Module location for entities that the Delegator knows about
#  Please compare to KnownEntities 
#  For module-loading, it needs to be in this key:value order
#  If you can merge these, please do so.
class subEntities(GemsStrEnum) :
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

