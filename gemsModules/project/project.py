#!/usr/bin/env python3
import logging
from datetime import datetime
from gemsModules.common.transaction import *
from gemsModules.project.settings import *
from pydantic import BaseModel, Schema
from pydantic.schema import schema

debugLevel=logging.DEBUG
logging.basicConfig(level=debugLevel, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

"""
The backend project is concerned with updating the transaction
with
"""
class Project(BaseModel):
    ##The time this project was created. Different from the frontend project,
    ##  and also different from job submission time.
    timestamp = ""  ##User uploads go here. This is provided by the frontend.
    input_dir =  ""  ##Module output goes in output_dir with this name. Create this on project instantiation. Use a uuid
    output_dir = ""  ##Who is requesting this project? Actual? LiveDev? JSON_API request? Command line? Dev Env?
    requesting_agent = ""  ##project_id comes from the frontend. It is the primary key in the project table of the django db
    project_id = "" ##Created by frontend
    md5sum = "" ##Created by frontend

    def buildProject(self, thisTransaction):
        logging.info("New project instantiation.")
        request = thisTransaction['request_dict']
        logging.info("thisTransaction['request_dict']: " + str(request))
        self.timestamp = request['project']['timestamp']
        if request['project']['input_dir']:
            self.input_dir = request['project']['input_dir']
        self.output_dir = settings.output_data_root + "tools/" + str(uuid.uuid4())
        ##TODO: Update frontend model to include indication of dev/actual/devEnv/json_api
        ##IF none present, assume requesting agent is command line.
        if request['project']['_dango_version']:
            self.requesting_agent = 'django'
        else:
            self.requesting_agent = 'unknown'
        if request['project']['id']:
            self.project_id = request['project']['id']
        if request['project']['md5sum']:
            self.md5sum = ['project']['md5sum']


    def __str__(self):
        return "\nProject created: " + str(self.timestamp) + "\n\tRequested by: " + self.requesting_agent + "\n\tinput_dir: " + self.input_dir + "\n\toutput_dir: " + self.output_dir + "\n"



    """
        "_state": "<django.db.models.base.ModelState object at 0x7f32fc401750>",
        "user_id": "2",
        "title": "Untitled project",
        "timestamp": "2019-12-11 14:54:36.117499+00:00",
        "id": "aeb8179c-0290-499f-a30b-967f9629fea8",
        "comment": " ",
        "type": "cb",
        "email": "",
        "gems_version": "2016xxx",
        "gmml_version": "2016yyy-2",
        "ff_version": "2012xxx",
        "parameter_version": "2014",
        "amber_version": "2014xxx",
        "root": " ",
        "project_ptr_id": "aeb8179c-0290-499f-a30b-967f9629fea8",
        "sequence": "DManpa1-6DManpa1-OH",
        "ion": "No",
        "solvation": "Yes",
        "solvation_size": "8",
        "solvation_distance": "2",
        "solvation_shape": "REC",
        "num_structures": "1",
        "linkage_info": "",
        "rotamer_info": "",
        "rotamer_list": "",
        "angle_info": "",
        "md5dir": " ",
        "md5sum": "349a1a9c122031e575816a662acc9471",
        "job_info": "",
        "toolDir": "/website/userdata/tools/cb",
        "path": "/cb/media",
        "_django_version": "2.2.2"
"""
