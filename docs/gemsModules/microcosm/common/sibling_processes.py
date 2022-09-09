#!/usr/bin/env python3
from abc import ABC, abstractmethod

from gemsModules.docs.microcosm.common.logger import Set_Up_Logging
Set_Up_Logging(__name__)

class Siblings(ABC) :
    @abstractmethod
    def get_sibling_type() :
        return str

    def __init__(self) :
        self.siblings : List[self.get_sibling_type()] = []
        self.ordered  : bool   = False

    def add_sibling(self, sibling) :
        self.siblings.append(sibling)


class Sibling_Tree(ABC) :
    def __init__(self) :
        self.siblings_list : List[Union[Siblings,List[Siblings]]] = [],

    def add_list(self, new_siblings_list) :
        self.siblings_list.append(new_siblings_list)
