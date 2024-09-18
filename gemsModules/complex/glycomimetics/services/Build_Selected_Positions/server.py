#!/usr/bin/env python3
from .api import Build_Selected_Positions_Request, Build_Selected_Positions_Response
from ..common_api import Position_Modification_Options
from .logic import execute

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(
    service: Build_Selected_Positions_Request,
) -> Build_Selected_Positions_Response:
    log.info(f"service: {service}")

    response = Build_Selected_Positions_Response()
    
    selected_position = service.inputs.Selected_Modification_Options
    if selected_position is None:
        # Check resources for a resourceRole: "Selected_Modification_Options"
        for r in service.inputs.resources:
            if r.resourceRole == "Selected_Modification_Options":
                log.debug("Found Selected_Modification_Opttions in resources...")
                selected_position = Position_Modification_Options(**r.get_payload())
                service.inputs.Selected_Modification_Options = selected_position
                break
        else:
            log.warning(f"No Position Selected, cannot run Glycomimetics/Build_Selected_Positions")
            response.notices.addNotice(
                Brief="No Position Selected",
                Scope="Build_Selected_Positions",
                Messenger="Glycomimetics",
                Type="Warning",
                Code="699",
                Message=f"No Position Selected, cannot run Glycomimetics"
            )     
            return response
        
    try:
        response.outputs = execute(service.inputs)
    except Exception as e:
        log.error(f"Error running Glycomimetics: {e}")
        # append notice
        response.notices.addNotice(
            Brief="Error running Glycomimetics",
            Scope="Build_Selected_Positions",
            Messenger="Glycomimetics",
            Type="Error",
            Code="700",
            Message=f"Error running Glycomimetics: {e}",
        )
        
    return response
