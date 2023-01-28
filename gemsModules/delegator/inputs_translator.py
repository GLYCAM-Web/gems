from gemsModules.common.main_api_services import Services
from gemsModules.delegator.main_api import Delegator_API
from gemsModules.delegator.services.marco.api import marco_Service

class input_translator: 

    def __init__(self, inputs: Delegator_API):
        self.inputs = inputs

    def translate(self):
        self.implied_services : Services = Services()
        if 'cake' in self.inputs.entity.inputs.keys() :
            this_service = marco_Service()
            this_service.inputs.entity='Delegator'
            this_service.inputs.who_I_am='Delegator'
            if this_service.options is None:
                this_service.options = {}
            this_service.options["cake"]=self.inputs.entity.inputs["cake"]
            if 'color' in self.inputs.entity.inputs.keys() :
                this_service.options["color"]=self.inputs.entity.inputs["color"]
            self.implied_services.add_service('cakeMarco',this_service)

            print("The implied services are:")
            print(self.implied_services)
