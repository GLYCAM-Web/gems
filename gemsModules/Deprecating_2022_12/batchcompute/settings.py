#!/usr/bin/env python3

## Who I am
WhoIAm='BatchCompute'

## Module names for services that this entity/module can perform.
## These should not include the Common Services.

##Status Report
status = "In development"
moduleStatusDetail = "Currently working on Gems/JSON interface."

servicesStatus = [
    {
        "service" : "Submit",
        "status" : "In development.",
        "statusDetail" : "Working on module architecture."
    }
]


## Module names for services that this entity/module can perform.
serviceModules = {
    "Submit" : "submit"
}


def main():
    print("Ths script only contains dictionary-type information.")

if __name__ == "__main__":
  main()

