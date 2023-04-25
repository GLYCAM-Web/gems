#!/usr/bin/env python3
from typing import Callable, List, Dict
import uuid

from gemsModules.common.code_utils import Annotated_List

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Action_Associated_Object_Package ():
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
        self.child_packages = None

    def __repr__(self):
        out_string = (f'ID_String = {self.ID_String}\n'
                f'AAO_Type = {self.AAO_Type}\n'
                f'Dictionary_Name = {self.Dictionary_Name}\n'
                f'The_AAO = {self.The_AAO!r}\n'
                f'Dependencies = {self.Dependencies!r}\n'
                )
        if self.child_packages is not None:
            out_string += f'child_packages = {self.child_packages!r}\n'
        return out_string

    def get_callable(self):
        return self.The_AAO

    def create_child_package_list(self,  
            items : List = [],
            ordered  : bool   = True,):
        self.child_packages = Annotated_List(items, ordered)

    def add_child_package(self, child_package) :
        if self.child_packages is None:
            self.create_child_package_list(self)
        self.child_packages.items.append(child_package)

    def get_child_packages(self) :
        return self.child_packages
    
    def get_linear_list(self) :
        """Return a list of all the AAOs in this AAOP, including any child packages.
           Also include child packages of child packages, etc.
           After that, remove the child packages from the list.
        """
        linear_list = []
        if self.child_packages is not None:
            for child_package in self.child_packages:
                additional_list=child_package.get_linear_list()
        new_self = self.make_skeleton_copy()
        new_self.child_packages = None
        linear_list.append(self)
        linear_list.extend(additional_list)
        return linear_list
    
    def make_skeleton_copy(self):
        """Create a new AAOP with the same ID_String, AAO_Type, Dictionary_Name,
           Dependencies, and skeleton copies of any child packages.
        """
        new_aaop = Action_Associated_Object_Package(
                ID_String = self.ID_String,
                AAO_Type = self.AAO_Type,
                Dictionary_Name = self.Dictionary_Name,
                Dependencies = self.Dependencies,
                )
        if self.child_packages is not None:
            new_aaop.create_child_package_list()
            new_aaop.child_packages.ordered = self.child_packages.ordered
            for child_package in self.child_packages:
                new_aaop.add_child_package(child_package.make_skeleton_copy())
        return new_aaop

    def make_deep_copy(self):
        """Create a new AAOP that is an exact duplicate of the current one, including
            any child packages.
        """
        new_aaop = Action_Associated_Object_Package(
                ID_String = self.ID_String,
                AAO_Type = self.AAO_Type,
                Dictionary_Name = self.Dictionary_Name,
                The_AAO = self.The_AAO,
                Dependencies = self.Dependencies,
                )
        if self.child_packages is not None:
            new_aaop.create_child_package_list()
            new_aaop.child_packages.ordered = self.child_packages.ordered
            for child_package in self.child_packages:
                new_aaop.add_child_package(child_package.make_deep_copy())
        return new_aaop


AAOP = Action_Associated_Object_Package


class AAOP_Tree() :
    """Tree of Action_Associated_Object_Packages
       The lists are the AAO packages associated with
       the action.

       packages = the complete list of packages

       Each package might contain other packages, so this is a tree.
    """
    def __init__(self, packages : Annotated_List) -> None :
        self.packages = packages
        self._current_AAOP_index = -1

    def __repr__(self):
        return f'packages = {self.packages!r}\n'

    def _next_AAOP(self, putme : AAOP = None): 
        """Get the next AAOP in the tree"""
        # For now we assume there is only a linear list of packages.
        # We will need special iterator, eventually.  
        # Need depth-first search, but each AAOP should be able to override that.
        print("in _next_AAOP.  appendme = ", putme)
        print("self.packages.items = ", self.packages.items)
        self._current_AAOP_index += 1
        if self._current_AAOP_index >= len(self.packages.items):
            raise StopIteration
        if putme is not None:
            self.packages.items[self._current_AAOP_index]=putme.copy(deep=True)
        else:
            return self.packages.items[self._current_AAOP_index]

    def get_next_AAOP (self) :
        """Return the next AAOP in the tree.  Set that as current."""
        print('about to get_next_AAOP')
        return self._next_AAOP(self)

    def put_next_AAOP (self, putme : AAOP) :
        """Write the AAOP to the next AAOP in the tree"""
        self._next_AAOP(appendme=putme)

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
        new_tree = AAOP_Tree(packages=Annotated_List())
        new_tree.packages.ordered = self.packages.ordered
        for package in self.packages:
            new_tree.packages.append(package.make_skeleton_copy())

    def make_deep_copy(self):  
        """Make a deep copy of the tree"""
        new_tree = AAOP_Tree(packages=Annotated_List())
        new_tree.packages.ordered = self.packages.ordered
        for package in self.packages:
            new_tree.packages.append(package.make_deep_copy())

    def make_linear_list(self) -> List:
        """Make a linear list of AAOPs in the tree"""
        new_list : List[AAOP] = []
        for package in self.packages:
            new_list.append(package)
            if package.child_packages is not None:
                for child_package in package.child_packages:
                    new_list.append(child_package)


class AAOP_Tree_Pair():
    """Holds a pair of AAOP Trees.  
       Typically one tree is input and the other is output.

       The output_callable_type_dictionary is a dictionary of types to callables.
       The type is the type of The_AAO in the incoming AAOP.  The callable is
       the function that will be called during generation of the output AAOP.
       """
    input_tree : AAOP_Tree  # input tree
    output_tree : AAOP_Tree # output tree
    outgoing_callable_type_dictionary : Dict[type, Callable] = None

    def __init__(self, input_tree: AAOP_Tree, output_tree: AAOP_Tree = None):
        self.input_tree = input_tree
        self.output_tree = output_tree

    def __repr__(self):
        return f'input_tree = {self.input_tree!r}\noutput_tree = {self.output_tree!r}\n'

    def generate_output_tree(self, deep_copy : bool = False):
        """Generate the output tree from the input tree"""
        if deep_copy == True:
            self.output_tree = self.input_tree.make_deep_copy()
        else:
            self.output_tree = self.input_tree.make_skeleton_copy()

    def get_next_AAOP_incoming(self):
        print("about to get_next_AAOP_incoming")
        self.input_current = self.input_tree.get_next_AAOP()
        print("got next AAOP incoming it is:")
        print(self.input_current)
        return self.input_current
    
    def put_next_AAOP_outgoing(self, putme : AAOP) -> None:
        self.output_tree.put_next_AAOP(putme)


