#!/usr/bin/env python3
from typing import Callable,List
from .main_api_services import Service 
from .code_utils import Annotated_List

from .logger import Set_Up_Logging
Set_Up_Logging(__name__)

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


