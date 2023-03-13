from gemsModules.delegator.redirector_settings import Known_Entities
from typing import List

def execute() -> List:
    """ Return a list of entities known to the Delegator
    >>> print(execute())
    ['Delegator', 'DeprecatedDelegator', 'MDaaS', 'Status', 'BatchCompute', 'Conjugate', 'Common', 'MmService', 'Query', 'Sequence', 'DrawGlycan', 'StructureFile']
    """

    return Known_Entities.get_json_list()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
