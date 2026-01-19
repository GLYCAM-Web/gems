from gemsModules.{{cookiecutter.gems_module}}.services.settings.known_available import Available_Services
from typing import List


def execute() -> List:
    """ Return a list of available services

    >>> print(execute())
    ['Error', 'Marco', 'Status', 'ListServices', '{{cookiecutter.service_name}}']

    """

    return Available_Services.get_json_list()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
