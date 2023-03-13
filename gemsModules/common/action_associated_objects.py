#!/usr/bin/env python3
from abc import ABC
from typing import Callable, List
import uuid


from gemsModules.common.code_utils import Annotated_List

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Action_Associated_Object_Package (ABC):
    """Package for an Action_Associated_Object (AAO)
        This class is abbreviated AAOP.

        An AAO is any object that is associated with some action.  For example,
            both Service Request objects and Response objects are objects that 
            are associated with an action.  The AAO package contains the
            object and metadata about the object.

       If the AAO_Type is 'AAOP_Tree', then The_AAO will remain none and the only
       components will be child_packages, ID_String and Dependencies.  This allows 
       for easy and annotated nesting of the AAOP Trees within each other. 
    """
    def __init__(self,
            ID_String : str = uuid.uuid4(), # free-form internal identifier, by default a UUID
            AAO_Type : str = 'Service', # type identifier, for convenience
            Dictionary_Name : str = None, # name given in the dictionary, if this came from one
            The_AAO : Callable = None,
            Dependencies : List[str] = None, # list of ID_Strings for AAOPs that must be executed before this one
            ) -> None :
        self.AAO_Type = AAO_Type
        self.ID_String = ID_String
        self.The_AAO = The_AAO
        self.Dictionary_Name = Dictionary_Name
        self.Dependencies = Dependencies

    def __str__(self):
        out_string = (f'ID_String = {self.ID_String}\n'
                f'AAO_Type = {self.AAO_Type}\n'
                f'Dictionary_Name = {self.Dictionary_Name}\n'
                f'The_AAO = {self.The_AAO!r}\n'
                f'Dependencies = {self.Dependencies!r}\n'
                )
        return out_string

#    def __print__(self):
#        print(repr(self))

    def create_child_package_list(self,  
            items : List = [],
            ordered  : bool   = True,):
        self.child_packages = Annotated_List(items, ordered)

    def add_child_package(self, child_package) :
        if self.child_packages is None:
            self.create_child_package_list(self)
        self.child_packages.append(child_package)

    def get_child_packages(self) :
        return self.child_packages


AAOP = Action_Associated_Object_Package


class AAOP_Tree(ABC) :
    """Tree of Action_Associated_Object_Packages
       The lists are the AAO packages associated with
       the action.

       packages = the complete list of packages
    """
    def __init__(self, packages : Annotated_List = None) -> None :
        self.packages = packages

    def _next_AAOP(self):
        """Get the next AAOP in the tree"""
        pass # might need special iterator, eventually.  Need depth-first-ish search.

    def get_next_AAOP (self, allow_parallel : bool = False) :
        """Return the next AAOP in the tree.  Set that as current."""
        self._current_AAOP = self._next_AAOP(self)
        return self.current_AAOP

    def put_current_AAOP (self, incoming_aaop) :
        """Write the AAOP to the next AAOP in the tree"""
        self._current_AAOP = incoming_aaop

#    def get_AAOP_by_ID (ID_String: str) :
#        """Get an AAOP by ID"""
#        #return self._temporary_AAOP
#        pass
#
#    def put_AAOP_by_ID (ID_String: str, incoming_aaop: AAOP) :
#        """Overwrite an AAOP by ID"""
#        #return self._temporary_AAOP
#        pass

    def make_skeleton_copy(self):
        """Make a skeleton copy of the tree"""
        pass

    def make_deep_copy(self):  
        """Make a deep copy of the tree"""
        pass

    def make_linear_list(self) -> List:
        """Make a linear list of AAOPs in the tree"""
        pass


class AAOP_Tree_Pair(ABC):
    """Holds a pair of AAOP Trees.  
       Typically one tree is input and the other is output.
       """
    input_tree : AAOP_Tree  # input tree
    output_tree : AAOP_Tree # output tree

    def __init__(self, input_tree: AAOP_Tree, output_tree: AAOP_Tree):
        self.input_tree = input_tree
        self.output_tree = output_tree

    def get_next_AAOP_pair(self):
        self.input_current = self.input_tree.get_next_AAOP()
        self.output_current = self.output_tree.get_next_AAOP()
        return self.input_current, self.output_current

    def put_output_current_AAOP(self, incoming_aaop: AAOP):
        self.output_tree.put_current_AAOP(incoming_aaop)

