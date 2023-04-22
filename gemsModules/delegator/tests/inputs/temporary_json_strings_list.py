#!/usr/bin/env python3

the_json_strings=[
"""{
 "entity" : {
    "type": "Delegator",
    "inputs" : { 
	    "cake" : "true", 
	    "color" : "bandearg" 
    }
  }
}""",
"""{
 "entity" : {
    "type": "Delegator",
    "services" :
        { "cakeMarco" :
                {
			"type" : "Marco" ,
			"options" : { 
				"cake" : "true", 
				"color" : "pink" 
			}
		 
		}
        }
  }
}""",
"""{
 "entity" : {
    "type": "Delegator",
    "inputs" : { 
	    "cake" : "true", 
	    "color" : "pink" 
    },
    "services" :
        { "cakeMarco" :
                {
			"type" : "Marco" ,
			"options" : { 
				"cake" : "false", 
				"color" : "purple" 
			}
		 
		}
        }
  }
}""",
"""{
 "entity" : {
    "type": "Delegator",
    "services" :
        { "cakeMarco" :
                {
			"type" : "Marco" ,
			"options" : { 
				"cake" : "true", 
				"color" : "pink" 
			}
		 
		}
        }
  }
}""",
"""{
 "entity" : {
    "type": "Delegator",
    "inputs" : { 
	    "cake" : "true", 
	    "color" : "pink" 
    }
  }
}""",
"""{
 "entity" : {
    "type": "Delegator"
  }
}""",
"""{
 "entity" : {
    "type": "Delegator",
    "services" :
        { "Marco" :
                {
			"type" : "Marco" 
		 
		}
        }
  }
}"""
]
