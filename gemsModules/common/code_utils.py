#!/usr/bin/env python3
from enum import Enum
from typing import  List

from gemsModules.common.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


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

class Annotated_List() :
    """ The purpose of this class is to provide list metadata.
        The list can be ordered or unordered.  The default is ordered.
        If set to ordered, it should be assumed that the items must be
        processed in the order they are listed.  If set to unordered,
        items can be processed in any order, or in parallel, etc.
        """
    def __init__(self,
            items : List = [],
            ordered  : bool   = True,
            ) -> None :
        self.items : List = items
        self.ordered  : bool = ordered

    def add_item(self, item) :
        self.items.append(item)

    def get_items(self) :
        return self.items

    def get_ordered(self) :
        return self.ordered

    def set_ordered(self, ordered) :   
        self.ordered = ordered

