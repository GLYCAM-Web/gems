from pydantic import Field
from gemsModules.common import main_api_services
from gemsModules.logging.logger import Set_Up_Logging

from .services.settings.known_available import Available_Services

log = Set_Up_Logging(__name__)

class PDBFile_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "PDBFile",
        alias="type",
        title="Services offered by PDB Entity",
        description="The service requested of the PDB Servicer",
    )


class PDBFile_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services offered by PDB Entity",
        description="The service response from PDB",
    )

