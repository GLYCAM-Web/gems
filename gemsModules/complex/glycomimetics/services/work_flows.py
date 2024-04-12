from gemsModules.common.services.workflow_manager import Service_Work_Flows_template
from gemsModules.common.services.workflow_manager import (
    Service_Work_Flow_Order_template,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def get_Service_Work_Flows() -> Service_Work_Flows_template:
    """Return services work Flows data"""

    from gemsModules.complex.glycomimetics.services import marco
    from gemsModules.complex.glycomimetics.services import list_services

    error_list = [error]
    list_services_list = [list_services]
    marco_list = [marco]
    build_list = [build]
    status_list = [status]

    Service_Work_Flows = Service_Work_Flows_template

    Service_Work_Flows.append(Service_Work_Flow_Order_template("error", error_list))
    Service_Work_Flows.append(Service_Work_Flow_Order_template("marco", marco_list))
    Service_Work_Flows.append(
        Service_Work_Flow_Order_template("list_services", list_services_list)
    )
    Service_Work_Flows.append(Service_Work_Flow_Order_template("status", status_list))
    Service_Work_Flows.append(Service_Work_Flow_Order_template("build", build_list))
    return Service_Work_Flows


def testme():
    """Test the workflows and get human-friendly output
        The part after the 'from' in the string'd module is removed for
        compatibility with multiple systems.
    >>> testme()
    -------------------------------------------------------------------------------
    -------------------------------------------------------------------------------
    The service work flows follow.
    -------------------------------------------------------------------------------
    Workflow type: marco
    Modules to call (services to run) :
        1 :  <module 'gemsModules.delegator.services.marco'
    -------------------------------------------------------------------------------
    Workflow type: list_services
    Modules to call (services to run) :
        1 :  <module 'gemsModules.delegator.services.list_services'
    -------------------------------------------------------------------------------
    -------------------------------------------------------------------------------
    """
    print(
        "-------------------------------------------------------------------------------"
    )
    print(
        "-------------------------------------------------------------------------------"
    )
    print("The service work flows follow.")
    print(
        "-------------------------------------------------------------------------------"
    )
    sep = "from"
    for workflow in get_Service_Work_Flows():
        print("Workflow type: " + str(workflow.Service_Type))
        print("Modules to call (services to run) :")
        count = 1
        for module in workflow.Operations_Order_List:
            print("    " + str(count) + " :  " + str(module).split(sep, 1)[0])
            count = count + 1
        print(
            "-------------------------------------------------------------------------------"
        )
    print(
        "-------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
