#!/usr/bin/env python3

## Who I am
WhoIAm='Delegator'

status = "Stable"
moduleStatusDetail = "Can Delegate and ListEntities."

servicesStatus = [
    {
        "service" : "delegate",
        "status" : "Stable.",
        "statusDetail" : "Can receive a request for an entity and service, validate the request, and forward the request to the appropriate entity."
    },
    {
        "service" : "ListEntities",
        "status" : "Stable.",
        "statusDetail" : "Simply lists the entities that have been developed."
    }
]


## Module names for services that this entity/module can perform.
## These should not include the Common Services.
ServiceModule = {  # probably will be deprecated
    'delegate' : 'delegate',
    'ListEntities' : 'listEntities',
}

# Names of available services in JSON mapped to internal names
AvailableServices = {
        'Delegate' 
        'ListEntities' 
        'Marco' 
        }

## Module names for entities that the Delegator knows about
subEntities = {
    'BatchCompute' : 'batchcompute',
    'CommonServices' : 'common',
    'Conjugate' : 'conjugate',
    'DrawGlycan' : 'drawglycan',
    'Glycoprotein' : 'conjugate',
    'MmService' : 'mmservice',
    'Query' : 'query',
    'Sequence' : 'sequence',
    'Status' : 'status',
    'StructureFile' : 'structureFile'
}




def main():
    print("Ths script only contains dictionary-type information.")

if __name__ == "__main__":
  main()
