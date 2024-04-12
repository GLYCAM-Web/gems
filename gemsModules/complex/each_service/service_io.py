from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, validator, Field

from gemsModules.common.code_utils import GemsStrEnum
from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.complex.each_service.known_available import (
    Glycomimetics_Allowed_File_Formats_Allowed_File_Formats,
)


class Glycomimetics_Allowed_File_Formats_Files_Resource(ABC, Resource):

    resourceFormat: str = Field(
        None,
        title="Resource Format",
        description="Formats supported for one of the Glycomimetics_Allowed_File_Formats entities.",
    )

    @validator("resourceFormat", pre=True, always=True)
    @abstractmethod
    def ensure_proper_formats(cls, v, values, **kwargs):
        if (
            v not in Glycomimetics_Allowed_File_Formats_Allowed_File_Formats
        ):  # replace with your own validation
            raise ValueError("Resource format not supported.")
        else:
            return v


class Glycomimetics_Allowed_File_Formats_Files_Resources(ABC, Resources):
    __root__: List[Glycomimetics_Allowed_File_Formats_Files_Resource] = None


class Glycomimetics_Allowed_File_Formats_Request_Inputs(ABC, BaseModel):
    inputFiles: Glycomimetics_Allowed_File_Formats_Files_Resources = None
    workingDirectory: str = None
    workGroup: str = None


class Glycomimetics_Allowed_File_Formats_Request_Outputs(ABC, BaseModel):
    pass
