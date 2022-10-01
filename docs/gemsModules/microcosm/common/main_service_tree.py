#!/usr/bin/env python3
from typing import Callable, List, Union
from .main_api_services import Service, Response
from .code_utils import GemsStrEnum
from .sibling_processes import Siblings, Sibling_Tree

from .logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Response_Next_State(GemsStrEnum) :
    Proceed = 'Proceed'
    StopChain = 'StopChain'
    StopAll = 'StopAll'


class Response_Status(GemsStrEnum) :
    OK = 'OK'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    UNKNOWN = 'UNKNOWN'


class Response_Package() :
    def __init__(self, 
            keyString : str,
            response : Response,
            status : Response_Status = 'OK',
            next_state : Response_Next_State = 'Proceed'
            ) :
        self.response = response
        self.keyString = keyString
        self.status = status
        self.next_state = next_state


class Service_Package() :
    def __init__(self,
            keyString : str,
            service : Service,
            server_Module: Callable
            ) -> None :
        self.service = service
        self.keyString = keyString
        self.server_Module = server_Module


class Siblings() :
    def __init__(self,
            siblings : List = [],
            ordered  : bool   = False
            ) -> None :
        self.siblings = siblings
        self.ordered  = ordered

    def add_sibling(self, sibling) :
        self.siblings.append(sibling)


class Sibling_Tree() :
    def __init__(self,
            siblings_list : List[Union[Siblings,List[Siblings]]] = [],
            ) -> None :
        self.siblings_list = siblings_list

    def add_list(self, siblings_list) :
        self.siblings_list.append(siblings_list)

