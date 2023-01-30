from gemsModules.common.services.orders_dependencies import Service_Work_Flows_template
from gemsModules.common.services.orders_dependencies import Service_Work_Flow_Order_template
from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

from gemsModules.delegator.services import marco
from gemsModules.delegator.services import known_entities
from gemsModules.delegator.services import list_services

class Available_Services(GemsStrEnum):
    Marco = 'Marco'
    Known_Entities = 'Known Entities'
    List_Services = 'List Services'


Multiples_Action={
    'Marco' : 'Merge'
    'Known_Entities' : 'Merge'
    'List_Services' :  'Merge'
    }

Request_Conflict_Action={
    'Marco' : 'Fail'
    'Known_Entities' : 'Ignore'
    'List_Services' :  'Ignore'
    }


## Workflows 
## Delegator's Services all have simple workflows
marco_list = [ marco ]
known_entities_list = [ known_entities ]
list_services_list = [ list_services ]

Service_Work_Flows = Service_Work_Flows_template

Service_Work_Flows.append(Service_Work_Flow_Order_template(
    "default", 
    marco_list
        ))
Service_Work_Flows.append(Service_Work_Flow_Order_template(
    "marco", 
    marco_list
        ))
Service_Work_Flows.append(Service_Work_Flow_Order_template(
    "known_entities", 
    known_entities_list
        ))
Service_Work_Flows.append(Service_Work_Flow_Order_template(
    "list_services", 
    list_services_list
        ))



#print("-------------------------------------------------------------------------------")
#print("-------------------------------------------------------------------------------")
#print("The service work flows follow.")
#print("-------------------------------------------------------------------------------")
#for workflow in Service_Work_Flows:
#    print("Workflow type: " + str(workflow.Service_Type))
#    print("Modules to call (services to run) :")
#    count=1
#    for module in workflow.Operations_Order_List: 
#      print("    " + str(count) + " :  " +  str(module))
#      count=count+1
#    print("-------------------------------------------------------------------------------")
#print("-------------------------------------------------------------------------------")
