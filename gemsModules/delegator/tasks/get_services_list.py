from gemsModules.delegator.services.services_settings import Available_Services
from typing import List

def execute() -> List:
    """ Return a list of entities known to the Delegator
    >>> print(execute())
    ['Marco', 'Known Entities', 'List Services']
    """

    return Available_Services.get_json_list()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
