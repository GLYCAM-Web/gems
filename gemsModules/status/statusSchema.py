from enum import Enum, auto
from pydantic import BaseModel, Field
from pydantic.schema import schema


"""
Status Report Request Schema Definitions
    Not currently in use, here to test moving subschemas
    into their modules.
"""
class StatusServicesEnum(str,Enum):
    generateReport = 'GenerateReport'

class StatusServices(BaseModel):
    statusServices : StatusServicesEnum = Field(
        'GenerateReport',
        title = 'Status Reporting Services',
        description = 'Reporting services for gemsModules.'
    )
