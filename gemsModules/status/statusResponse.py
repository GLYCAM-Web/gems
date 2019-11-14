#!/usr/bin/env python3
from typing import Dict, List
from pydantic import BaseModel, Schema
from pydantic.schema import schema

"""Whole class is experimental"""
class ServiceReport(BaseModel):
    service : str
    status : str
    statusDetail : str


class StatusResponse(BaseModel):
    entity : str
    status : str
    moduleStatusDetail : str
    serviceReports : List[ServiceReport]

def createDummyServiceReport():
    report1 = ServiceReport(service='Build3DStructure', status='Up', statusDetail='meh')
    print("report1: " + str(report1))

    report2 = ServiceReport(service='Validate', status='Up', statusDetail='meh')
    print("report2: " + str(report2))

    reports = [report1, report2]
    statusResponse = StatusResponse(entity="Sequence", status='Up', moduleStatusDetail='Stuff happening.', serviceReports=reports)
    print("statusResponse.status: " + str(statusResponse))
    return statusResponse

def printDummyStatusResponse():
    response1 = createDummyServiceReport()
    response2 = createDummyServiceReport()
    responses = [response1, response2]
    print("responses: " + str(responses))

if __name__ == "__main__":
    printDummyStatusResponse()
