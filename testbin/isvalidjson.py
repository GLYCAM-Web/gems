#!/usr/bin/env python3
# consumed by pre-push test 009
# confirms if response from delegator is valid json

import sys
import json
import traceback

try: 
	filepath = sys.argv[1]
except:
	print("must supply file path as argv[1]")
	exit(2)

try:
	with open(filepath) as f:
		try:
			string = f.read()			
			jsonstring = json.loads(string)			
			exit(0)
		except Exception as error:			
			exit(1)
except Exception as err:
	string  = "could not open " + filepath
	print(string)
	print(traceback.format_exc())
	exit(2)



