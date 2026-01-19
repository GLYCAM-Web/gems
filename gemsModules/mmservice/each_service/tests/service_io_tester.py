from typing import List
from pydantic import validator
from gemsModules.mmservice.each_service import service_io
from gemsModules.mmservice.each_service import known_available

class local_Files_Resource(service_io.Mmservice_Files_Resource):
    """
    The local version of the mmservice files resource.
    """

    @validator('resourceFormat', pre=True, always=True)
    def ensure_proper_formats(cls, v, values, **kwargs):
        if v not in known_available.Mmservice_Allowed_File_Formats.get_json_list():  # replace with your own validation
            raise ValueError ("Resource format not supported.")
        else:
            return v

class local_Files_Resources(service_io.mmservice_Files_Resources):
    """
    The local version of the mmservice files resources.
    """
    __root__ : List[local_Files_Resource] = None

class local_Request_Inputs(service_io.Mmservice_Request_Inputs):
    """
    The local version of the mmservice request inputs.
    """
    inputFiles : local_Files_Resources = None
    workingDirectory : str = None
    workGroup : str = None


test_json_input="""
{
    "workingDirectory": "/home/username/Downloads",
    "workGroup": "myWorkGroup",
    "inputFiles": [
        {
            "resourceFormat": "PDB",
            "typename": "PDB File",
            "locationType" : "filesystem-path-unix",
            "payload": "/home/username/Downloads/1crn.pdb"
        } 
    ]
}
"""

def test_local_Request_Inputs():
    theInputs = local_Request_Inputs.parse_raw(test_json_input)
    print(theInputs.json(indent=2))


if __name__ == "__main__":
    test_local_Request_Inputs()
