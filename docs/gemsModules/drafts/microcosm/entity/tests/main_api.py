#!/usr/bin/env python3
from gemsModules.docs.microcosm.entity import main_api

transaction = main_api.Module_Transaction()
print("The schema type is: " + str(transaction.get_API_type()))
transaction.generateSchema()
