#!/usr/bin/env python3
import os
from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.services.marco.request_translator import marco_request_translator

#test_files_list = [ 
#        os.path.join('inputs', 'caca_milis.json'), 
#        os.path.join('inputs', 'cake_explicit_fiddling.json'),
#        os.path.join('inputs', 'cake_explicit_implicit.json'),
#        os.path.join('inputs', 'cake_explicit.json'),
#        os.path.join('inputs', 'cake_implied.json'),
#        os.path.join('inputs', 'default.json'),
#        os.path.join('inputs', 'marco_explicit.json'),
#        ]

from gemsModules.delegator.tests.inputs.temporary_json_strings_list import the_json_strings

for i in the_json_strings :
    this_transaction = Delegator_Transaction()
    this_transaction.process_incoming_string(in_string=i)
    translator = marco_request_translator(this_transaction)
    the_aaop_list = translator.process()
    print("---------------------------------------------------------------")
    print(" input file:   " + str(i))
    print("---------------------------------------------------------------")
    print("here is each item in the aaop list")
    for item in the_aaop_list :
        print(item)
    print("---------------------------------------------------------------")


