from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Available_Services(GemsStrEnum):
    Marco = 'Marco'
    Known_Entities = 'Known Entities'
    List_Services = 'List Services'


Multiples_Action={
    'Marco' : 'Merge',
    'Known_Entities' : 'Merge',
    'List_Services' :  'Merge'
    }

Request_Conflict_Action={
    'Marco' : 'Fail',
    'Known_Entities' : 'Ignore',
    'List_Services' :  'Ignore'
    }


