from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.common.services.settings.known_available import Available_Services as Common_Available_Services


from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Module_Available_Services(GemsStrEnum):
    run_md = 'RunMD'

Available_Services = GemsStrEnum(
    "Available_Services",
    [(avail.name, avail.value) for avail in Common_Available_Services] + 
    [(avail.name, avail.value) for avail in Module_Available_Services] 
)



def testme():
    """ Ensure that the settings info is complete.
    >>> testme()
    ['Error', 'Marco', 'Status', 'ListServices', 'RunMD']

    """
    print(Available_Services.get_json_list())


if __name__ == "__main__":
    import doctest
    doctest.testmod()

