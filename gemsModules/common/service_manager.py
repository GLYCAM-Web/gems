from gemsModules.common.action_associated_objects import AAOP_Tree
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

##########################################################################
## 
##       The word SERVICE is the enemy...
##
##########################################################################

class Service_Manager():

    def __init__(self, transaction: Transaction):
        pass

    def process(self):
        self.translate_incoming_data_into_service_packages(self)
        self.add_explicit_service_packages(self)
        self.fill_transaction_level_data(self)

##  Move all this to the servicer - let services fill in prereqs (service chain??  sigh...)
        self.build_service_request_package_tree(self)
        self.build_skeleton_service_response_tree(self)
        self.build_service_tree_set(self)
        self.call_servicer(self)
## After this we need transaction-level knowledge again

        self.build_transaction_outputs(self)
        self.add_top_level_outputs(self)

## These two go up in a higher level bc more info might get added
##        self.generate_outgoing_string(self)
##        self.return_outgoing_string(self)

    def translate_incoming_data_into_service_packages(self):
        pass

    def add_explicit_service_packages(self):
        pass

    def build_service_request_package_tree(self):
        pass

    def fill_transaction_level_data(self):
        pass

    def build_skeleton_service_response_tree(self):
        pass

    def build_service_tree_set(self):
        pass

    def call_servicer(self):
        pass

    def build_transaction_outputs(self):
        pass

    def generate_outgoing_string(self):
        pass

    def return_outgoing_string(self):
        pass



### Step 6:  Build Tree Set

### Step 7:  Send Tree Set to Servicer to have the services be run





        self.implied_service_packages: Service_Package = self.translate_incoming_data(self.transaction)
### Notes:

    ##  Unless required somehow, do not clobber information in a Service Request.

### Step 1:  Hand to the Input Data translator.  It does this:

    ## For each entry in the 'Inputs' part of the Transaction, it looks to see
        ##  which Services are implied.  

    ## Creates Service_Request_Packages for each implied Service

    ## Copy in whatever info is in the Inputs

    ## Tag that service as implied.  "serviceOrigin" : "Implied"

### Step 2:   Hand to a service filler.  The filler does this:

    ## Make Service_Request_Packages from each explicit Services in the list.
        ##  Tag as serviceOrigin = Explicit

### Step 3:  Build the AAOP Service_Request_Tree.  Do these things:

    ## Copies in global info like "force serial execution" and "md minimize = false".

    ## Merges and arranges services in Service_Request_Packages
        ##  Sort and/or merge Services
            ## Explicit services override all
            ## Make class so conditions for overriding can happen later.  
    
    ## Insert prerequisite services as needed.  Tag as serviceOrigin = Requisite

### Step 4:  Fill required data into each Service_Request_Package 

    ## Each service must know its own data.

### Step 5:  Instantiate and fill a skeleton Service_Response_Tree

### Step 6:  Build Tree Set

### Step 7:  Send Tree Set to Servicer to have the services be run

    ## Each service might consist of multiple tasks, but the service keeps up with that

    ## Additional data filling can happen in the service as needed


