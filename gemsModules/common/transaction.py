#!/usr/bin/env python3
from collections import defaultdict
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from pydantic import BaseModel, Schema
from pydantic.schema import schema

# ####
# ####  Enums
# ####

# ##
# ## Enums for Entity-specific Services
# ##
class DelegatorServicesEnum(str,Enum):
    delegate = 'Delegate' 

class DelegatorServices(BaseModel):
    delegatorServices : DelegatorServicesEnum = Schema(
            'Delegate',
            title = 'Delegator  Services',
            description = 'Services available to the Delegator Entity'
            )

class SequenceServicesEnum(str,Enum):
    build3DStructure = 'Build3DStructure'

class SequenceServices(BaseModel):
    sequenceServices : SequenceServicesEnum = Schema(
            'Build3DStructure',
            title = 'Sequence  Services',
            description = 'Services available to the Sequence Entity'
            )

class GlycoProteinServicesEnum(str,Enum):
    build3DStructure = 'Build3DStructure'

class GlycoProteinServices(BaseModel):
    glycoProteinServices : GlycoProteinServicesEnum = Schema(
            'Build3DStructure',
            title = 'GlycoProtein  Services',
            description = 'Services available to the GlycoProtein Entity'
            )

# ##
# ## Enums relevant to all Entities & Services
# ##
class EntityTypeEnum(str, Enum):
    delegator = 'Delegator'
    sequence = 'Sequence'
    commonServices = 'CommonServices'
    glycoprotein = 'Glycoprotein'
    structureFile = 'StructureFile'

class CommonServicesEnum(str,Enum):
    """
    Services used by all Entities.

    The behaviors of these services might differ from one Entity to another.  
    For example, 'ListServices' or 'DefaultService' will certainly differ.  
    Even something like 'Marco', which will look the same on the surface, 
    will return 'Polo' for the relevant Entity.

    On that note, there is a 'CommonServices' Entity.  If the incoming JSON
    object is sufficiently malformed, this is the Entity that responds.

    See the Enums for each specific service, above.
    """
    marco = 'Marco'
    evaluate = 'Evaluate'
    listEntities = 'ListEntities'
    listServices = 'ListEntities' 
    returnHelp = 'ReturnHelp'
    returnSchema = 'ReturnSchema'
    defaultService = 'DefaultService'

class CommonServices(BaseModel):
    commonServices : CommonServicesEnum = Schema(
            'DefaultService',
            title = 'Common Services',
            description = 'Services available to all Entities'
            )

# ##
# ## Other general Enums
# ##
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
    """Holds information about a requested Service."""
    typename : Union[CommonServices, DelegatorServices, SequenceServices, GlycoProteinServices] = Schema(
            None,
            title='Type of Service.',
            description='The services available will vary by Entity.'
            )
    options : List[Option] = Schema(
            None,
            title = 'Options for this service',
            description = 'Options might be specific to the Entity and/or Service.  See docs.'
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
    ## TODO: figure out how to include a list of Entities in the Entity itself.
#    entities : List['Entity'] = None

#Entity.update_forward_refs()

class Project(BaseModel):
    resources : List[Resource] = None

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


#print(Entity.schema_json(indent=2))
top_level_schema = schema([Entity, Project], title='A GemsModules Transaction')
def generateGemsModulesSchema():
    import json
    print(json.dumps(top_level_schema, indent=2))

if __name__ == "__main__":
  generateGemsModulesSchema() 
#print(Resource.schema_json(indent=2))
