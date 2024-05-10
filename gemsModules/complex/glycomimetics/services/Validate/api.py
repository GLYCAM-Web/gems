#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.complex.glycomimetics.main_api import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Validate_input_Resource(Resource):
    """Need to write validators."""

    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | md_path | max_hours
    ##
    ## payload = string containing a /path/to/file  |  integer (number of hours)
    ##
    ## options = none currently read
    ##
    pass


class Validate_output_Resource(Resource):
    """Need to write validators."""

    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | amber_nc | amber_mdcrd | amber_mdout | zipfile
    ##
    ## payload = string containing a /path/to/file
    ##
    ## notices = these will surely happen
    ##
    pass


class Validate_Resources(Resources):
    __root__: List[Union[Validate_input_Resource, Validate_output_Resource]] = None


class Validate_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    resources: Validate_Resources = Validate_Resources()

    # Note: The problem with using a validator here is we can't easily return the results in the Response.
    @validator("resources", always=False)
    def check_resources(cls, v):
        has_cocomplex_input = False
        has_moiety_metadata = False
        has_execution_parameters = False
        for resource in v.__root__:
            if resource.resourceRole == "cocomplex-input":
                has_cocomplex_input = True
            elif resource.resourceRole == "moiety-metadata":
                has_moiety_metadata = True
            elif resource.resourceRole == "execution-parameters":
                has_execution_parameters = True
            else:
                log.warning(f"Unknown resource role: {resource.resourceRole}")

        if not (
            has_cocomplex_input and has_moiety_metadata and has_execution_parameters
        ):
            raise ValidationError(
                "All required resources (cocomplex-input, moiety-metadata, execution-parameters) must be provided."
            )
        return v


class Validate_Outputs(BaseModel):
    outputDirPath: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    isValid: bool = Field(
        None,
        title="Is Valid",
        description="Is the input valid",
    )


class Validate_Request(Glycomimetics_Service_Request):
    typename: str = Field("Validate", alias="type")
    # the following must be redefined in a child class
    inputs: Validate_Inputs = Validate_Inputs()


class Validate_Response(Glycomimetics_Service_Response):
    typename: str = Field("Validate", alias="type")
    outputs: Validate_Outputs = Validate_Outputs()
