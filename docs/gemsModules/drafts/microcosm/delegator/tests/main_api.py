#!/usr/bin/env python3
from gemsModules.docs.microcosm.delegator import main_api

transaction = main_api.Delegator_Transaction()
print(transaction.generate_schema())
