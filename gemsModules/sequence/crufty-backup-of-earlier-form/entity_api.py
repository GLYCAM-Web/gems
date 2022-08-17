#!/usr/bin/env python3
import gemsModules.common.common_api as commonio
import gemsModules.project.project_api as projectio
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class sequenceEntity(commonio.Entity):
    """Holds information about the main object responsible for a service."""
    services: Dict[str, sequenceService] = sequenceService()
    inputs: SequenceInputs = None
    outputs: SequenceOutputs = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.info("Instantiating a sequenceEntity")
        log.debug("entityType: " + self.entityType)

class SequenceAPI(commonio.CommonAPI):
    """
    Holds info about the top-level JSON API object used in the Sequence entity.
    """
    entity: sequenceEntity = ...   # ... means a value is required in Pydantic.
    project: projectio.CbProject = None

#    def __init__(self, **data: Any):
#        super().__init__(**data)

    class Config:
        title = 'gensModulesSequenceAPI'


class SequenceTransaction(commonio.Transaction):
    def get_API_type(self):
        return SequenceAPI
#    from gemsModules.sequence._manageSequenceBuild3DStructureRequest import manageSequenceBuild3DStructureRequest

def generateSchema():
    print(SequenceAPI.schema_json(indent=2))


inputJSON = '{ "entity": { "type": "Sequence", "services":  { "Build": { "type": "Build3DStructure" } } , "inputs":  { "Sequence": { "payload": "DManpa1-OH" } } } }'


def troubleshoot():
    thisTransaction = Transaction(inputJSON)
    print(thisTransaction.incoming_string)
    print(thisTransaction.request_dict)
    thisTransaction.populate_transaction_in()
    print(thisTransaction.transaction_in)


if __name__ == "__main__":
    generateSchema()
    troubleshoot()
