#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.services.each_service.manage_multiples import Multiples_Manager
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.common.services.marco.api import marco_Request

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class marco_Multiples_Manager(Multiples_Manager):

    def process_multiples(self) -> List[AAOP]:
        return self.process_multiples_action_Merge()

    def process_multiples_action_Merge(self):
        merge_conflict = False
        first_aaop = self.incoming_aaop_list[0]
        for aaop in self.incoming_aaop_list[1:]:
            merged_aaop = self.merge_aaop(first_aaop, aaop)
            log.debug("merged_aaop is" + str(merged_aaop))
            if merged_aaop is None:
                merge_conflict = True
                self.processed_aaop_list.extend(self.process_conflicted_merge())
                log.debug("self.processed_aaop_list is " + str(self.processed_aaop_list))
                break
        if merge_conflict == False:
            log.debug("no merge conflict")
            self.processed_aaop_list.extend(merged_aaop)
        return self.processed_aaop_list

    def process_conflicted_merge(self):
        this_request = marco_Request(typename='Marco')
        this_request.inputs.entity = 'Delegator'
        this_request.inputs.who_I_am = 'Delegator'
        this_request.options = {}
        this_request.options['merge_conflict'] = 'Merge conflict'
        this_request.options['info'] = 'Conflicting information was sent to Marco'
        this_aaop = AAOP(ID_String=str(uuid.uuid4()),
                Dictionary_Name='Marco_Error', 
                The_AAO=this_request,
                AAO_Type='Error')
        return [this_aaop]


    def merge_aaop(self, aaop1, aaop2):
        log.debug("Merging aaop1 and aaop2")
        request1 = aaop1.The_AAO
        request2 = aaop2.The_AAO
        log.debug("request1 is " + str(request1))
        log.debug("request2 is " + str(request2))
        # if request1.inputs.entity != request2.inputs.entity:
        #     print("entities are different")
        #     return None
        # print("about to check who_I_am")
        # if request1.inputs.who_I_am != request2.inputs.who_I_am:
        #     return None
        if "cake" in request1.options and "cake" in request2.options:
            if request1.options["cake"] != request2.options["cake"]:
                return None
        elif "cake" in request2.options:
            request1.options["cake"] = request2.options["cake"]
        if "color" in request1.options and "color" in request2.options:
            if request1.options["color"] != request2.options["color"]:
                return None
        elif "color" in request2.options:
            request1.options["color"] = request2.options["color"]
        if "merge_conflict" in request1.options and "merge_conflict" in request2.options:  # this is a merge conflict
            return None  # and wonder how we ever got to this code...
        aaop1.The_AAO = request1
        return [aaop1]
