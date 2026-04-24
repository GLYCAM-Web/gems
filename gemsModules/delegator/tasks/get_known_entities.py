from gemsModules.delegator.redirector_settings import get_known_entities
from typing import List

def execute() -> List:
    """ Return a list of entities known to the Delegator
    >>> print(execute())
    ['MDaaS', 'MmService', 'Status', 'PDBFile', 'AntibodyDocking', 'Glycomimetics', 'GlycoProtein', 'BatchCompute', 'Conjugate', 'DeprecatedDelegator', 'DrawGlycan', 'Query', 'Sequence', 'StructureFile']
    """

    return str(get_known_entities())

if __name__ == "__main__":
    import doctest
    doctest.testmod()
