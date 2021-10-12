#!/usr/bin/env python3
# consumed by pre-push test 009
# confirms if response from delegator is valid json

import sys
import json
import traceback

try: 
	testOutput = sys.argv[1]
	correctOutput = sys.argv[2]
except:
	print("must supply file paths for argv[1] and argv[2]")
	exit(2)

try:
	with open(testOutput) as f:
		try:
			string = f.read()			
			test = json.loads(string)			
			exit(0)
		except Exception as error:	
			string = "json.loads() failed -- problem with JSON: " + testOutput		
			exit(1)
except Exception as err:
	string  = "could not open " + filepath
	print(string)
	print(traceback.format_exc())
	exit(2)

try:
	with open(testOutput) as f:
		try:
			string = f.read()			
			correct = json.loads(string)			
			exit(0)
		except Exception as error:	
			string = "json.loads() failed -- problem with JSON: " + testOutput		
			exit(1)
except Exception as err:
	string  = "could not open " + filepath
	print(string)
	print(traceback.format_exc())
	exit(2)