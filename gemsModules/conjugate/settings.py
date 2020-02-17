#!/usr/bin/env python3

## Who I am
WhoIAm='Conjugate'

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
    }
]

subEntities = [
    {
        "subEntity" : "StructureFile"
    }
]

## Module names for services that this entity/module can perform.
serviceModules = {
    "BuildGlycoprotein" : "buildGlycoprotein"
}


def main():
    print("Ths script only contains dictionary-type information.")

if __name__ == "__main__":
  main()

