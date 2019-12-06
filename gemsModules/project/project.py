#!/usr/bin/env python3
import logging
from datetime import datetime

debugLevel=logging.DEBUG
logging.basicConfig(level=debugLevel, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


"""
The backend project is concerned with updating the transaction
with
"""
class Project():
    ##The time this project was created. Different from the frontend project,
    ##  and also different from job submission time.
    timestamp = ""
    ##User uploads go here. This is provided by the frontend.
    input_dir =  ""
    ##Module output goes here. Create this on project instantiation. Use a uuid
    output_dir = ""
    ##Who is requesting this project? Actual? LiveDev? JSON_API request? Command line? Dev Env?
    requesting_agent = ""

    def __init__(self, input_dir, output_dir, requesting_agent):
        logging.info("New project instantiation.")
        self.timestamp = str(datetime.now())
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.requesting_agent = requesting_agent

    def __str__(self):
        return "\nProject created: " + str(self.timestamp) + "\n\tRequested by: " + self.requesting_agent + "\n\tinput_dir: " + self.input_dir + "\n\toutput_dir: " + self.output_dir + "\n"

