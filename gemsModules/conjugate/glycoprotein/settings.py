#!/usr/bin/env python3
from enum import Enum, auto

## Who I am
WhoIAm='GlycoProtein'

## Module names for services that this entity/module can perform.
## These should not include the Common Services.

##Status Report
status = "In development"
moduleStatusDetail = "Currently working on Gems/JSON interface."

servicesStatus = [
    {
        "service" : "BuildGlycoprotein",
        "status" : "In development.",
        "statusDetail" : "Working on receiving json api requests."
    },
    {
        "service" : "Evaluate",
        "status" : "In development.",
        "statusDetail" : "Working on receiving json api requests."
    },
    {
        "service" : "Status",
        "status" : "In development.",
        "statusDetail" : "Working on receiving json api requests."
    }
]

subEntities = [
    {
        "subEntity" : "StructureFile",
        "subEntity" : "Sequence"
    }
]

## Module names for services that this entity/module can perform.
serviceModules = {
    "BuildGlycoprotein" : "buildGlycoprotein",
    "Evaluate" : "evaluate",
    "Status" : "status"
}

# ##
# ## Services
# ##
class Services(str,Enum):
    buildGlycoprotein = 'BuildGlycoprotein'
    evaluate = 'Evaluate'
    status = 'Status'


def main():
    print("Ths script only contains dictionary-type information.")

if __name__ == "__main__":
  main()

