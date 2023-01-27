from gemsModules.common.action_associated_objects import AAOP_Tree
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Service_AAOP_Set():
    def __init__(self):
        self.Request_Tree=AAOP_Tree()

    def initialize_response_tree(self):
        self.Response_Tree = self.Request_Tree.make_skeleton_copy()

    def add_request(self):
        return self.Request_Tree.

    def get_response_tree(self):
        return self.Response_Tree

    def get_next_service_set(self) -> (AAOP, AAOP):
        pass
