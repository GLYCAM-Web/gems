#!/usr/bin/env python3

## Who I am
WhoIAm='Delegator'

"""
Module names for services that this entity/module can perform.
These should not include the Common Services.
"""

ServiceModule = {
    'delegate' : 'delegate',
    'ListEntities' : 'listEntities',
}

"""
Module names for entities that the Delegator knows about
"""
entityModules = {
    'Conjugate' : 'conjugate',
    'Common' : 'common',
    'Query' : 'query',
    'Sequence' : 'sequence',
    'DrawGlycan' : 'drawglycan',
}


def main():
    print("Ths script only contains dictionary-type information.")

if __name__ == "__main__":
  main()

