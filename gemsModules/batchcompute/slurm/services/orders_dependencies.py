from collections import namedtuple
from typing import List

from gemsModules.common.loggingConfig import *
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

from gemsModules.batchcompute.slurm.services import route_to_host, build_submission_script, submit_job, query_job
#from gemsModules.common import 



Service_Work_Flow_Order = namedtuple(
        "Service_Work_Flow_Order",
            "Service_Type Task_List")
Service_Work_Flows : List[Service_Work_Flow_Order] = []

return_supported_services_list = [ ]
submit_job_list = [ route_to_host, build_submission_script, submit_job ]
query_list = [ route_to_host, query_job ]

Service_Work_Flows.append(Service_Work_Flow_Order(
    "default", 
    return_supported_services_list
        ))

Service_Work_Flows.append(Service_Work_Flow_Order(
    "job submission", 
    submit_job_list
        ))

Service_Work_Flows.append(Service_Work_Flow_Order(
    "job query", 
    query_list
        ))

print("-------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------")
print("The service work flows follow.")
print("-------------------------------------------------------------------------------")
for workflow in Service_Work_Flows:
    print("Workflow type: " + str(workflow.Service_Type))
    print("Modules to call (services to run) :")
    count=1
    for module in workflow.Task_List: 
      print("    " + str(count) + " :  " +  str(module))
      count=count+1
    print("-------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------")
