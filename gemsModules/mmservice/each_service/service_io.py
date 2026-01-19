from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, validator, Field

from gemsModules.common.code_utils import GemsStrEnum
from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.mmservice.each_service.known_available import Mmservice_Allowed_File_Formats

class Mmservice_Files_Resource(ABC, Resource):
    
    resourceFormat : str  = Field(
            None, 
            title = 'Resource Format',
            description = 'Formats supported for one of the mmservice entities.'
            )

    @validator('resourceFormat', pre=True, always=True)
    @abstractmethod
    def ensure_proper_formats(cls, v, values, **kwargs):
        if v not in Mmservice_Allowed_File_Formats:  # replace with your own validation
            raise ValueError ("Resource format not supported.")
        else:
            return v

class mmservice_Files_Resources(ABC, Resources):
    __root__ : List[Mmservice_Files_Resource] = None

class Mmservice_Request_Inputs(ABC, BaseModel):
    inputFiles : mmservice_Files_Resources = None
    workingDirectory : str = None
    workGroup : str = None



class Mmservice_Request_Outputs(ABC, BaseModel):
    pass

