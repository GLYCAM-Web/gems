#!/usr/bin/env python3
from pydantic import BaseModel, Field
from gemsModules.common.loggingConfig import *
import traceback


if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


class TheSequence(BaseModel):
    payload: str = ''
    sequenceFormat: str = Field(
        'GlycamCondensed',
        alias='format',
        description='The format of the sequence in the payload'
    )

    class Config:
        title = 'Sequence'


class TheSequenceVariants(BaseModel):
    """Different representations of the sequence."""
    # condensed sequence types
    indexOrdered: str = None  # key is 'indexOrdered' ???
    longestChainOrdered: str = None
    userOrdered: str = None
    monospacedTextDiagram: str = None
    # ... labeled
    indexOrderedLabeled: str = None
    longestChainOrderedLabeled: str = None
    userOrderedLabeled: str = None
    monospacedTextDiagramLabeled: str = None
    # other condensed sequence representations
    suuid: str = None
    smd5sum: str = None

    # ## I'm certain there is a better way to do this.  - Lachele
    def getSequenceVariant(self, variant):
        log.info("TheSequenceVariants.getSequenceVariant was called")
        theVariant = getattr(self, variant)
        return theVariant


def generateSchema():
    import json
    print(TheSequenceVariants.schema_json(indent=2))


if __name__ == "__main__":
    generateSchema()
