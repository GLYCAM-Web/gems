import unittest
import json
from receive import receive

default_in = '{ "entity" : { "type": "Status" } }'

def get_string_from_receive(input):
    return receive(input)

class TestStatusModule(unittest.TestCase):
    
    def test_receive_returns_string(self):
        assert isinstance(get_string_from_receive(default_in), str)
    
    def test_receive_returns_json_formatted_string(self):    
        assert isinstance(json.loads(default_in), object) #prove default_in is valud .json
        assert isinstance(json.loads(get_string_from_receive(default_in)), object)
        
        
