#!/usr/bin/env python3
from enum import Enum

from gemsModules.docs.microcosm.common.logger import Set_Up_Logging
Set_Up_Logging(__name__)


class GemsStrEnum(str, Enum):
    """
    A base class for all String-based Gems Enumerations.

    The additions simplify some uses of Enums that are convenient, particularly
    since our classes interact with Pydantic.
    """

    @classmethod
    def get_list(self):
        return self.get_value_list()

    @classmethod
    def get_json_list(self):
        return self.get_value_list()

    @classmethod
    def get_value_list(self):
        theList = []
        for item in self :
            theList.append(item.value)
        return theList

    @classmethod
    def get_key_list(self):
        return self.get_name_list()

    @classmethod
    def get_internal_list(self):
        return self.get_value_list()

    @classmethod
    def get_name_list(self):
        theList = []
        for item in self :
            theList.append(item.name)
        return theList


