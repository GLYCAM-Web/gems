from typing import List

from ..services.settings.known_available import Available_Services


def execute() -> List:
    """Return a list of available services

    >>> print(execute())
    []

    """

    return Available_Services.get_json_list()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
