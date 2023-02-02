from gemsModules.common.services.orders_dependencies import Service_Work_Flows_template
from gemsModules.common.services.orders_dependencies import Service_Work_Flow_Order_template


from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


from gemsModules.delegator.services import marco
from gemsModules.delegator.services import known_entities


the_marco_list = [ marco ]
the_known_entities_list = [ known_entities ]

Service_Work_Flows = Service_Work_Flows_template

Service_Work_Flows.append(Service_Work_Flow_Order_template(
    "default", 
    the_marco_list
        ))
Service_Work_Flows.append(Service_Work_Flow_Order_template(
    "marco", 
    the_marco_list
        ))
Service_Work_Flows.append(Service_Work_Flow_Order_template(
    "known_entities", 
    the_known_entities_list
        ))

print("-------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------")
print("The service work flows follow.")
print("-------------------------------------------------------------------------------")
for workflow in Service_Work_Flows:
    print("Workflow type: " + str(workflow.Service_Type))
    print("Modules to call (services to run) :")
    count=1
    for module in workflow.Operations_Order_List: 
      print("    " + str(count) + " :  " +  str(module))
      count=count+1
    print("-------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------")
