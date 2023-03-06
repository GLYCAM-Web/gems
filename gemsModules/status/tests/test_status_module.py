import unittest
import json
from receive import receive

_default_in = '{ "entity" : { "type": "Status" } }'

##
#@detail
# write me
def _get_string_from_receive(input: str) -> str:
    return receive(input)

##
#@detail
# write me
class TestStatusModule(unittest.TestCase):
    ##
    #@brief
    # assert receive() returns a str
    def test_receive_returns_string(self):
        assert isinstance(_get_string_from_receive(_default_in), str)
    
    ##
    #@detail
    # assert receive() default_in is .json formatted str
    # assert receive() returns a .json formatted str
    def test_receive_returns_json_formatted_string(self):        
        assert isinstance(json.loads(_default_in), object) #prove default_in is valud .json
        assert isinstance(json.loads(_get_string_from_receive(_default_in)), object)
        
        
