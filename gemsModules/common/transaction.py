#!/usr/bin/env python3
from collections import defaultdict
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema
from pydantic.schema import schema

# ####
# ####  Enums
# ####
class EntityTypeEnum(str, Enum):
    delegator = 'Delegator'
    sequence = 'Sequence'
    commonServices = 'CommonServices'
    glycoprotein = 'Glycoprotein'
    structureFile = 'StructureFile'

class CommonServices(str,Enum):
    marco = 'Marco'
    evaluate = 'Evaluate'
    listEntities = 'ListEntities'
    returnHelp = 'ReturnHelp'
    returnSchema = 'ReturnSchema'

class ExternalLocationTypeEnum(str, Enum):
    filepath = 'file-path'
    httpheader = 'http-header'
    uri = 'uri'

class ExternalFormatEnum(str, Enum):
    pdb = 'PDB'
    mmcif = 'MMCIF'
    text = 'TEXT'
    amberoff = 'AMBEROFF' 

class ResourceStringFormatEnum(str, Enum):
    json = 'JSON'
    pdbid = 'PDBID'
    uri = 'URI' 
    glycamCondensed = 'GlycamCondensed' 
    glytoucanAccessionID = 'GlyTouCanID'
    glycamSequenceID = 'GlycamSequenceID'
    glycamNickName = 'GlycamNickName'

class NoticeTypeEnum(str, Enum):
    note = 'Note'
    warning = 'Warning'
    error = 'Error'
    exit = 'Exit'

# ####
# ####  Definition Objects
# ####
class ExternalResource(BaseModel):
    locationType: ExternalLocationTypeEnum = Schema(
            None,
            title='External Location Type',
            description='The kind of location that is specified in the Payload.'
            )
    resourceFormat: ExternalFormatEnum = Schema(
            None,
            title='Resource Format',
            description='The format of the external data.',
            )

class EmbeddedResource(BaseModel):
    resourceFormat: ResourceStringFormatEnum = Schema(
            ResourceStringFormatEnum.glycamCondensed,
            title='Resource Format',
            description='The format of the data embedded in the Payload.'
            )
    
class ResourceDescriptor(BaseModel):
    """Metadata about the resource (where, what, etc.)."""
    descriptor: Union[EmbeddedResource,ExternalResource] 

class Resource(BaseModel):
    """Information describing a resource containing data."""
    metadata : ResourceDescriptor = Schema(
            None
            )
    payload : str = Schema(
        None,
        description='The thing that is described in the Descriptor'
        )
    tags : List[Dict[str,str]] = Schema(
        None,
        description='List of arbitrary Key:Value pairs initially interpreted as string literals.'
        )

class Notice(BaseModel):
    """Description of a Notice."""
    noticeType: NoticeTypeEnum = Schema(
            None,
            title='Type',
            )
    noticeCode: str = Schema(
            None,
            title='Code',
            description='Code associated with this notice.'
            )
    noticeBrief: str = Schema(
            None,
            title='Brief',
            description='Brief title, status or name for this notice or notice type.'
            )
    noticeMessage : str = Schema(
            None,
            title='Message',
            description='A more detailed message for this notice.'
            )

class Option(BaseModel):
    """A key-value pair used to hold information about an option."""
    def __init__(self, key, value):
        """This might not need to be a whole class."""
        self.key = key
        self.value = value


class Service(BaseModel):
    """
    Storage for information relevant to performing a particular service.

    The Service is type-named based on the information in the request.  That
    name is then mapped to a submodule that performs the service.  Any 
    options or resources needed are also tracked.
    """
    typename : str = Schema(
            None,
            title='Type of Service.',
            description='The services available will vary by Entity.'
            )
    options : List[Option] = Schema(
            None,
            )
    inputs : List[Resource] = None
    requestID : str = Schema(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )

class Response(BaseModel):
    """Holds information about a response to a service request."""
    typename : str = Schema(
            None,
            title='Type of Service.',
            description='The type service that this is in response to.'
            )
    notices : List[Notice] = Schema(
            None
            )
    outputs : List[Resource] = None
    requestID : str = Schema(
            None,
            title = 'Request ID',
            description = 'User-specified ID from the service request.'
            )

# ####
# ####  Top-Level Objects
# ####
class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType: EntityTypeEnum = Schema(
            None,
            title='Type',
            )
    options : List[Option] = Schema(
            None,
            )
    inputs : List[Resource] = None
    requestID : str = Schema(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    services : List[Service] = None
    responses : List[Response] = None
#    entities : List['Entity'] = None

#Entity.update_forward_refs()

class Project(BaseModel):
    pass 

# ####
# ####  Container for use in the modules
# ####
class Transaction:
    """Holds information relevant to a delegated transaction"""
    from . import Entity, Option, Project
    def __init__(self, incoming_string):
        """
        Storage for the input and output relevant to the transaction.

        A copy of the incoming string is stored.  That string is parsed
        into a request dictionary.  As the entities perform their services,
        the response dictionary is built up.  From that the outgoing string
        is generated.
        """
        self.incoming_string = incoming_string
        self.request_dict = {}
        self.entity = Entity
        self.options = Options
        self.project = Project
        self.response_dict = {}
        self.outgoing_string = ""
    def build_outgoing_string():
        import json
        if ('jsonObjectOutputFormat','Pretty') in self.options.items():
            self.outgoing_string=json.dumps(response_dict, indent=4)
        else:
            self.outgoing_string=json.dumps(response_dict)


print(Entity.schema_json(indent=2))
#top_level_schema = schema([Entity, Project], title='A GemsModules Transaction')
#def generateGemsModulesSchema():
    #print(json.dumps(top_level_schema, indent=2))

#if __name__ == "__main__":
#  main() 
#print(Resource.schema_json(indent=2))
