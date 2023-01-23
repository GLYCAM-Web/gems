#!/usr/bin/env python3
from abc import ABC
from typing import Callable, List

from gemsModules.common.code_utils import Annotated_List

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class AAOP_Tree(ABC) :
    """Tree of Action_Associated_Object_Packages
       The lists are the AAO packages associated with
       the action.
    """
    def __init__(self,
            packages : Annotated_List = None
            ) -> None :
        self.packages = packages

    def _get_next_AAOP (self, allow_parallel : bool = False) :
        """Get the next AAOP in the tree"""
        pass    

    def get_AAOP_by_ID (ID_String) :
        """Get the AAOP by ID"""
        pass

    def write_to_next_AAOP (AAOP) :
        """Write the AAOP to the next AAOP in the tree"""
        pass

    def make_skeleton_copy(self) :
        """Make a skeleton copy of the tree"""
        pass

    def make_deep_copy(self) :  
        """Make a deep copy of the tree"""
        pass

    def make_linear_list(self) :
        """Make a linear list of AAOPs in the tree"""
        pass

    # need dunder method for '+' operator
    def __add__(self, other) :
        """Add two AAOP_Trees"""
        pass


class Action_Associated_Object_Package (ABC):
    """Package for an Action_Associated_Object (AAO)
        This class is abbreviated AAOP.

        An AAO is any object that is associated with some action.  For example,
            both Service objects and Response objects are objects that are 
            associated with an action.  The AAO package contains the
            object and metadata about the object.

       If the AAO_Type is 'AAOP_Tree', then The_AAO will remain none and the only
       components will be child_packages, ID_String and Dependencies.  This allows 
       for easy and annotated nesting of the AAOP Trees within each other. 
    """
    def __init__(self,
            ID_String : str = None, # free-form internal identifier
            AAO_type : str = 'Service', # free-form type identifier
            The_AAO : Callable = None,
            Dependencies : List[str] = None, # list of ID_Strings for AAOPs that must be executed before this one
            ) -> None :
        self.AAO_type = AAO_type
        self.ID_String = ID_String
        self.The_AAO = The_AAO
        self.Dependencies = Dependencies

    def add_child_package(self, child_package) :
        if self.child_packages is None : 
            self.child_packages = AAOP_Tree()
        self.child_packages.write_to_next_AAOP(child_package)

    def get_child_packages(self) :
        return self.child_packages

    def add_package_tree(self, package_tree : AAOP_Tree) :
        if self.child_packages is None : 
            self.child_packages = package_tree 
        else :
            self.child_packages = self.child_packages + package_tree # this probably needs mods

AAOP = Action_Associated_Object_Package



