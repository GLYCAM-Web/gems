#!/usr/bin/env python3
from sequence.entity_api import SequenceTransaction
from sequence.settings import ServiceModules, Operation_Order
from sequence.servicer_api import Sequence_Service


class Sequence_Servicer:
    def __init__(self, transaction: SequenceTransaction):
        self.transaction = transaction

    def delegate_services(self):
        if len(self.transaction.inputs.entity.services) == 0 :
            self.transaction = ServiceModules.Default(self.transaction)
            return self.transaction
        for service in Operation_Order:
            for name, service_object : Sequence_Service  in self.transaction.inputs.entity.services.items():
                if service_object.typename == service:
                    self.transaction = ServiceModules[name]service_object[name](self.transaction) # not the syntax yet
        return self.transaction
