#!/usr/bin/env python3
# consumed by pre-push test 009
# confirms if response from delegator is valid json

import sys
import json
import traceback

##### make sure 2 args are present #####
try: 
	testOutput = sys.argv[1]
	correctOutput = sys.argv[2]
except:
	print("must supply file paths for argv[1] and argv[2]")
	print(traceback.format_exc())
	exit(2)

##### read in argv[1], arv[2] #####
try:
	with open(testOutput) as f:
		try:
			string = f.read()			
			test = json.loads(string)						
		except Exception as error:	
			string = "json.loads() failed -- problem with JSON: " + testOutput		
			print(string)
			print(traceback.format_exc())
			exit(2)
except Exception as err:
	string  = "could not open " + filepath
	print(string)
	print(traceback.format_exc())
	exit(2)

try:
	with open(correctOutput) as f:
		try:
			string = f.read()			
			correct = json.loads(string)			
		except Exception as error:	
			string = "json.loads() failed -- problem with JSON: " + testOutput		
			print(string)
			print(traceback.format_exc())
			exit(2)
except Exception as err:
	string  = "could not open " + filepath
	print(string)
	print(traceback.format_exc())
	exit(2)

##### prune stuff that will be host-specific #####
remove = ["timestamp", "gems_timestamp", "site_version", "site_branch", "gems_version",
"gems_branch", "md_utils_version", "md_utils_branch", "gmml_version", "gmml_branch",
"gp_version", "gp_branch", "site_mode", "site_host_name"]


for thing in remove:
	del test["project"][thing]
	del correct["project"][thing]

##### compare the dictionaries #####
print (test==correct)


