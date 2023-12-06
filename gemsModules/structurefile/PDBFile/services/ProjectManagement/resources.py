import shutil
from pathlib import Path

from pydantic.typing import Literal, Optional

from pydantic import BaseModel, Field

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: Combine with Resource class from common.main_api_resources.
class PM_Resource(Resource):
    """A resource is a unified data object handler useful for converting and saving payloads between various formats."""

    typename: str = Field(
        "PM_Resource",
        alias="type",
        title="Resource type",
        description="The name of the type of Resource.",
    )


class ProjectManagement_Resources(Resources):
    __root__: list[PM_Resource] = None
