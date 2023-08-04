#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.action_associated_objects import AAOP_Tree_Pair
from gemsModules.common.main_api import Transaction
from gemsModules.common.project_manager import common_Project_Manager
from gemsModules.common.services.request_manager import common_Request_Manager
from gemsModules.common.services.response_manager import common_Response_Manager
from gemsModules.common.services.workflow_manager import common_Workflow_Manager
from gemsModules.common.services.aaop_tree_pair_manager import AAOP_Tree_Pair_Generator
from gemsModules.common.services.servicer import commonservices_Servicer

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Transaction_Manager(ABC):
    """Manages a Transaction."""

    def __init__(self, transaction: Transaction):
        # Transaction
        self.transaction = transaction
        self.incoming_entity = transaction.inputs.entity
        self.incoming_project = transaction.inputs.project
        self.response_entity = None
        self.response_project = None

        self.aaop_request_list: List[AAOP] = []
        self.aaop_tree_pair: AAOP_Tree_Pair = None

        # Local Modules
        self.request_manager = None
        self.response_manager = None
        self.aaop_tree_pair_manager = None
        self.project_manager = None
        self.this_servicer = None

        self.set_local_modules()

    @abstractmethod
    def set_local_modules(self):
        """Set the local modules.

        Must override this method in a subclass to define your custom Entity's local modules.
        """
        self.request_manager_type = common_Request_Manager
        self.aaop_tree_pair_manager_type = AAOP_Tree_Pair_Generator
        self.this_servicer_type = commonservices_Servicer
        self.response_manager_type = common_Response_Manager
        self.project_manager_type = common_Project_Manager

    def process(self):
        """Process the incoming entity and project bundled in a new Transaction."""
        log.debug("Processing transaction")

        self.manage_requests()
        self.generate_aaop_tree_pair()
        self.manage_project()
        self.invoke_servicer()
        self.manage_responses()
        self.update_transaction()

        log.debug("about to return transaction")
        return self.transaction

    def manage_requests(self):
        """Manage the Transaction's Requests from the incoming Entity."""
        log.debug("about to manage requests")

        self.request_manager = self.request_manager_type(entity=self.incoming_entity)
        self.aaop_request_list: List[AAOP] = self.request_manager.process()

        log.debug("\tthe aaop request list is: %s", self.aaop_request_list)

    # TODO: Move to end of request_manager.process?

    def generate_aaop_tree_pair(self):
        """Generate the AAOP Tree Pair from the AAOP Request List."""
        log.debug("about to generate aaop tree pair")

        self.aaop_tree_pair_manager = self.aaop_tree_pair_manager_type(
            aaop_request_list=self.aaop_request_list
        )
        self.aaop_tree_pair: AAOP_Tree_Pair = self.aaop_tree_pair_manager.process()

        log.debug("\tthe tree pair is: ")
        log.debug(self.aaop_tree_pair)

    def manage_project(self):
        """Manage the Response project using information from the incoming Entity and incoming Project."""
        log.debug("about to manage project")

        self.project_manager = self.project_manager_type(
            incoming_project=self.incoming_project, entity=self.incoming_entity
        )
        self.response_project = self.project_manager.process()
        self.request_manager.set_response_project(self.response_project)

        self.request_manager.fill_request_data_needs(self.transaction)
        log.debug(self.aaop_request_list)

    def invoke_servicer(self):
        """Invoke the Servicer.

        This will update the Response Tree in the AAOP Tree Pair by actually running the services on the Request Tree.
        """
        log.debug("about to invoke the following servicer: %s", self.this_servicer_type)

        self.this_servicer = self.this_servicer_type(tree_pair=self.aaop_tree_pair)
        log.debug("\tabout to serve")
        self.aaop_tree_pair = self.this_servicer.serve()

        log.debug("\tafter serving, the tree pair is: ")
        log.debug(self.aaop_tree_pair)

    def manage_responses(self):
        """Manage the Responses.

        This will generate the Response Entity from the Response Tree in the AAOP Tree Pair.
        """
        log.debug("about to manage responses")

        self.response_manager = self.response_manager_type(
            aaop_tree_pair=self.aaop_tree_pair
        )
        self.response_entity = self.response_manager.process()

        log.debug("\tthe response entity is: ")
        log.debug(self.response_entity)

    def update_transaction(self):
        """Update the Transaction from the Response Entity."""
        log.debug("about to update transaction")

        # get transaction outputs from response entity
        this_json = {"entity": self.response_entity.dict(by_alias=True)}
        self.transaction.outputs = self.transaction.get_API_type().parse_obj(this_json)

        # update transaction response project
        if self.response_project is not None:
            self.transaction.outputs.project = self.response_project.copy(deep=True)

        log.debug("\tthe transaction outputs are: ")
        log.debug(self.transaction.outputs.json(indent=2, by_alias=True))
