from gemsModules.structurefile.PDBFile.services.settings.known_available import (
    Available_Services,
)
from typing import List


def execute() -> List:
    """Return a list of available services

    >>> print(execute())
    ['AmberMDPrep', 'ProjectManagement']

    """

    return Available_Services.get_json_list()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
