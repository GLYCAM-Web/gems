#!/usr/bin/env python3
# import from typing first, in case you want to import pydantic.typing
from pathlib import Path
from typing_extensions import Literal, Optional
from pydantic import BaseModel, Field

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.structurefile.PDBFile.main_api import (
    PDBFile_Service_Request,
    PDBFile_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: Combine with Resource class from common.main_api_resources.
class PM_Resource(BaseModel):
    """A resource is a unified data object handler useful for converting and saving payloads between various formats."""

    name: str = Field(
        None,
        title="Resource Name",
        description="Name of resource",
    )
    res_format: str = Field(
        None,
        title="Resource Format",
        description="Format of resource",
    )
    location: Optional[str] = Field(
        "",
        title="Resource Location",
        description="Location of resource",
    )
    locationType: Literal["File", "InMemory"] = Field(
        None,
        title="Resource Location Type",
        description="Location type of resource",
    )

    def __init__(self, **data):
        payload = data.pop("payload", None)
        super().__init__(**data)
        # So that we don't include the payload in the basemodel, as it could be quite large and varied.
        object.__setattr__(self, "_payload", payload)

    @property
    def payload(self):
        return self._payload

    @property
    def filename(self) -> str:
        return f"{self.name}.{self.res_format}"

    def write(self, path: Path = None):
        if path is not None:
            if isinstance(path, str):
                path = Path(path)
            if path.exists():
                raise FileExistsError(f"File {path} already exists")
            with open(path, "w") as f:
                f.write(self._payload)
        else:
            raise ValueError("Must provide path")

    def load(self, path: Path = None, payload: str = None):
        if path is not None:
            if isinstance(path, str):
                path = Path(path)
            if not path.exists():
                raise FileNotFoundError(f"Could not find file {path}")
            with open(path, "r") as f:
                # TODO: Fix this terrible hack to get around the fact that the payload is a property that isn't included in the basemodel.
                object.__setattr__(self, "_payload", f.read())
        elif payload is not None:
            object.__setattr__(self, "_payload", payload)
        else:
            raise ValueError("Must provide either path or payload")

    def copy_to(self, path: Path):
        if isinstance(path, str):
            path = Path(path)

        path = path / self.filename

        # ensure that the payload is loaded
        if self._payload is None:
            if self.locationType == "File":
                self.load(path=Path(self.location) / self.filename)

        if self._payload is not None:
            log.debug(f"Copying resource {self.name} to {path}...")
            self.write(path)
        else:
            log.warning(f"Resource {self.name} has no payload to copy.")

    @classmethod
    def from_payload(cls, payload: str, name: str, res_format: str):
        obj = cls(
            name=name,
            locationType="InMemory",
            res_format=res_format,
            payload=payload,
        )
        return obj


class ProjectManagement_Resources(BaseModel):
    __root__: list[PM_Resource] = None


class ProjectManagement_Inputs(BaseModel):
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    projectDir: Optional[str] = Field(
        None,
        title="Project Directory",
        description="Full path to project directory",
    )
    resources: list[PM_Resource] = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=list,
    )


class ProjectManagement_Outputs(BaseModel):
    outputFilePath: str = Field(
        None,
        title="Output File Path",
        description="Full path to output file",
    )
    resources: ProjectManagement_Resources = ProjectManagement_Resources()


class ProjectManagement_Request(PDBFile_Service_Request):
    typename: str = Field("ProjectManagement", alias="type")
    # Cannot Make a PM request without inputs.
    inputs: ProjectManagement_Inputs = ProjectManagement_Inputs()


class ProjectManagement_Response(PDBFile_Service_Response):
    typename: str = Field("ProjectManagement", alias="type")
    outputs: ProjectManagement_Outputs = ProjectManagement_Outputs()
