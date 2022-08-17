#!/usr/bin/env python3
from gemsModules.docs.microcosm.common.main_api import Transaction
from gemsModules.docs.microcosm.common.main_api_services import Service, Services
from gemsModules.docs.microcosm.common.main_settings import All_Available_Services
from gemsModules.docs.microcosm.common.main_servicer_settings import All_Service_Modules

class Servicer:
    def __init__(self, transaction : Transaction):
        self.transaction = transaction

    def delegate_services(self):
        service_object : Service
        services : Services = self.transaction.get_input_services()
        if len(services) == 0 :
            All_Service_Modules.Default.value.Serve(self.transaction)
            return self.transaction
        # The following will break if anyone requests more than one of the 
        # same type of service in a single transaction.
        for service in All_Available_Services :  
            for service_object  in services.items().values():
                if service_object.typename == service:
                    self.transaction = All_Service_Modules.service.value.Serve(self.transaction) # not the syntax yet
        return self.transaction
