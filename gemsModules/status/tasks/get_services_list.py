#!/usr/bin/env python3

from gemsModules.delegator.services.settings import Available_Services
from typing import List

def execute() -> List:
    """ Return a list of available services

    >>> print(execute())
    ['Marco', 'Status', 'ListServices', 'Poll']

    """

    return Available_Services.get_json_list()

if __name__ == "__main__":
    import doctest
    doctest.testmod()