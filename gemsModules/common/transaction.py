#!/usr/bin/env python3
from enum import Enum, auto
from typing import Dict, List, Optional, Sequence, Set, Tuple, Union
from typing import ForwardRef
from pydantic import BaseModel, Schema
from pydantic.schema import schema

# ####
# ####  Enums
# ####
# ####  Keep values in some sort of logical order, please
# ####  Alphabetical is good if there is no other obvious order.
# ####

# ##
# ## Enums for Entity-specific Services
# ##
class DelegatorServicesEnum(str,Enum):
    delegate = 'Delegate'

class GlycoProteinServicesEnum(str,Enum):
    build3DStructure = 'Build3DStructure'

class SequenceServicesEnum(str,Enum):
    build3DStructure = 'Build3DStructure'

# ##
# ## Enums for environment variables
# ##
class SequenceServicesPathEnum(str,Enum):
    ## The entity itself
    sequenceentity   = 'GEMS_MODULES_SEQUENCE_PATH'
    ## Services for this entity, in alphabetical order
    build3DStructure = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'
    drawGlycan       = 'GEMS_MODULES_SEQUENCE_DRAWGLYCAN_PATH'
    evaluate         = 'GEMS_MODULES_SEQUENCE_STRUCTURE_PATH'

# ##
# ## Enums relevant to all Entities & Services
# ##
class EntityTypeEnum(str, Enum):
    commonServices = 'CommonServices'
    conjugate = 'Conjugate'
    delegator = 'Delegator'
    glycoprotein = 'Glycoprotein'
    sequence = 'Sequence'
    structureFile = 'StructureFile'
    query = 'Query'

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
    evaluate = 'Evaluate'
    defaultService = 'DefaultService'
    marco = 'Marco'
    listEntities = 'ListEntities'
    listServices = 'ListServices'
    returnHelp = 'ReturnHelp'
    returnSchema = 'ReturnSchema'

# ##
# ## Other general Enums
# ##
class ExternalFormatEnum(str, Enum):
    pdb = 'PDB'
    mmcif = 'MMCIF'
    text = 'TEXT'
    amberoff = 'AMBEROFF'

class ExternalLocationTypeEnum(str, Enum):
    filepath = 'file-path'
    httpheader = 'http-header'
    uri = 'uri'

class NoticeTypeEnum(str, Enum):
    note = 'Note'
    warning = 'Warning'
    error = 'Error'
    exit = 'Exit'

class ResourceStringFormatEnum(str, Enum):
    json = 'JSON'
    pdbid = 'PDBID'
    uri = 'URI'
    glycamCondensed = 'GlycamCondensed'
    glytoucanAccessionID = 'GlyTouCanID'
    glycamSequenceID = 'GlycamSequenceID'
    glycamNickName = 'GlycamNickName'

# ####
# ####  Definition Objects
# ####
# ####  The order will be guided mostly by dependency
# ####
class Tags(BaseModel):
    options : Dict[str,str] = Schema(
            None,
            description='Key-value pairs that are specific to each entity, service, etc'
            )

class DelegatorServices(BaseModel):
    delegatorServices : DelegatorServicesEnum = Schema(
            'Delegate',
            title = 'Delegator  Services',
            description = 'Services available to the Delegator Entity'
            )

class SequenceServices(BaseModel):
    sequenceServices : SequenceServicesEnum = Schema(
            'Build3DStructure',
            title = 'Sequence  Services',
            description = 'Services available to the Sequence Entity'
            )

class CommonServices(BaseModel):
    commonServices : CommonServicesEnum = Schema(
            'DefaultService',
            title = 'Common Services',
            description = 'Services available to all Entities'
            )

class GlycoProteinServices(BaseModel):
    glycoProteinServices : GlycoProteinServicesEnum = Schema(
            'Build3DStructure',
            title = 'GlycoProtein  Services',
            description = 'Services available to the GlycoProtein Entity'
            )

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
    options : Tags = None

class EmbeddedResource(BaseModel):
    resourceFormat: ResourceStringFormatEnum = Schema(
            ResourceStringFormatEnum.glycamCondensed,
            title='Resource Format',
            description='The format of the data embedded in the Payload.'
            )
    options : Tags = None
    
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
    options : Tags = None

class Notice(BaseModel):
    """Description of a Notice."""
    noticeType: NoticeTypeEnum = Schema(
            None,
            title='Type',
            alias='type'
            )
    noticeCode: str = Schema(
            None,
            title='Code',
            alias='code',
            description='Code associated with this notice.'
            )
    noticeBrief: str = Schema(
            None,
            title='Brief',
            alias='brief',
            description='Brief title, status or name for this notice or notice type.'
            )
    noticeMessage : str = Schema(
            None,
            title='Message',
            alias='message',
            description='A more detailed message for this notice.'
            )
    options : Tags = None

class Service(BaseModel):
    """Holds information about a requested Service."""
    typename : Union[CommonServices, DelegatorServices, SequenceServices, GlycoProteinServices] = Schema(
            None,
            title='Type of Service.',
            alias='type',
            description='The services available will vary by Entity.'
            )
    inputs : List[Resource] = None
    requestID : str = Schema(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    options : Tags = None

class Response(BaseModel):
    """Holds information about a response to a service request."""
    typename : str = Schema(
            None,
            title='Type of Service.',
            alias='type',
            description='The type service that this is in response to.'
            )
    notice : Notice = Schema(
            None
            )
    outputs : List[Resource] = None
    requestID : str = Schema(
            None,
            title = 'Request ID',
            description = 'User-specified ID from the service request.'
            )
    options : Tags = None

# ####
# ####  Top-Level Objects
# ####
class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType: EntityTypeEnum = Schema(
            ...,
            title='Type',
            alias='type'
            )
    inputs : List[Resource] = None
    requestID : str = Schema(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    ## TODO: Figure out the syntax so that it isn't necessaary 
    ## to say 'service : ' or 'response: ' before each.
    services : List[Service] = None
    responses : List[Response] = None
    options : Tags = None
     ## TODO: include a list of Entities once the recursion-schema bug is fixed.
#    entities : List['Entity'] = None

#Entity.update_forward_refs()

class Project(BaseModel):
    resources : List[Resource] = None
    options : Tags = None

class TransactionSchema(BaseModel):
    entity : Entity
    project : Project = None
    options : Tags = None

# ####
# ####  Container for use in the modules
# ####
class Transaction:
    """Holds information relevant to a delegated transaction"""
    def __init__(self, incoming_string):
        """
        Storage for the input and output relevant to the transaction.

        A copy of the incoming string is stored.  That string is parsed
        into a request dictionary.  As the entities perform their services,
        the response dictionary is built up.  From that the outgoing string
        is generated.
        """
        self.incoming_string = incoming_string
        self.request_dict : {} = None
        self.transaction_in : TransactionSchema = None
        self.transaction_out : TransactionSchema = None
        self.response_dict : {} = None
        self.outgoing_string : str = None

    def build_outgoing_string(self):
        import json
        isPretty=False
#        ## TODO: read in whether the output should be pretty
#        # this might work:
#        if self.transaction_in.options is not None:
#            if ('jsonObjectOutputFormat', 'Pretty') in self.transaction_in.options:
#                isPretty = True
        if isPretty:
            self.outgoing_string=json.dumps(self.response_dict, indent=4)
        else:
            self.outgoing_string=json.dumps(self.response_dict)

    def build_general_error_output(self):
        print("build_general_error_output was called. Still in development.")

#top_level_schema = schema([Entity, Project], title='A GemsModules Transaction')
def generateGemsModulesSchema():
    import json
    print(TransactionSchema.schema_json(indent=2))

if __name__ == "__main__":
  generateGemsModulesSchema()
