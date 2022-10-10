#!/usr/bin/env python3
from enum import Enum
from typing import  List

from .logger import Set_Up_Logging
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

# The purpose of this class is to provide list metadata so that the
# list can be ordered or unordered.  The default is ordered.
# An unordered list might contain items that are executable and can
# be executed in any order, or in parallel, etc.
# If they are set as fire-and-forget, then the order is not important,
# but they should also be executed in separate threads.
class Annotated_List() :
    def __init__(self,
            items : List = [],
            ordered  : bool   = True,
            fire_and_forget : bool = False
            ) -> None :
        self.items : List = items
        self.ordered  : bool = ordered
        self.fire_and_forget : bool = fire_and_forget

    def add_item(self, item) :
        self.items.append(item)

    def get_items(self) :
        return self.items

    def get_ordered(self) :
        return self.ordered

    def set_ordered(self, ordered) :   
        self.ordered = ordered

    def get_fire_and_forget(self) :
        return self.fire_and_forget

    def set_fire_and_forget(self, fire_and_forget) :   
        self.fire_and_forget = fire_and_forget