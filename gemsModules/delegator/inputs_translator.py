from gemsModules.common.main_api_services import Services

class input_translator: 

    def __init__(self, api: Delegator_API):
        self.api = api

    def translate(self):
        self.implied_services : Services = Services()
        if 'cake' in self.api.inputs.keys() :
            self.implied_services.append(Marco_Service)
