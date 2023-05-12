#!/usr/bin/env python3
from typing import Callable
from .main_api_services import Service, Response
from .code_utils import Annotated_List, GemsStrEnum

from .logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Service_Package :
    def __init__(self,
            keyString : str,
            service_Callable : Callable,
            service : Service,
            server_Module: Callable,
            child_packages : Annotated_List = Annotated_List()
            ) -> None :
        self.service = service
        self.service_Callable = service_Callable
        self.keyString = keyString
        self.server_Module = server_Module
        self.child_packages = child_packages

    def add_child_package(self, child_package) :
        self.child_packages.add_item(child_package)


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
            next_state : Response_Next_State = 'Proceed',
            child_packages : Annotated_List = Annotated_List()
            ) :
        self.response = response
        self.keyString = keyString
        self.status = status
        self.next_state = next_state
        self.child_packages = child_packages


class Service_Package_Tree(Annotated_List) :
    ...

class Response_Package_Tree(Annotated_List) :
    ...

