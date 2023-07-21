from gemsModules.common.main_api_notices import Notices
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(cls: "AmberMDPrep_Response_Manager") -> "AmberMDPrep_Response_Manager":
    request_aaop_list = cls.aaop_tree_pair.input_tree.make_linear_list()
    response_aaop_list = cls.aaop_tree_pair.output_tree.make_linear_list()
    log.debug(
        "the request aaop list is: %s\nthe response aaop list is: %s",
        request_aaop_list,
        response_aaop_list,
    )
    for aaop in request_aaop_list:
        this_service = aaop.The_AAO.copy(deep=True)
        this_service.myUuid = aaop.ID_String
        cls.response_entity.services.add_service(
            key_string=aaop.Dictionary_Name, service=this_service
        )
    for aaop in response_aaop_list:
        this_response = aaop.The_AAO.copy(deep=True)
        this_response.myUuid = aaop.ID_String
        this_response.notices = Notices()
        cls.response_entity.responses.add_response(
            key_string=aaop.Dictionary_Name, response=this_response
        )

    log.debug("the response entity is: ")
    log.debug(cls.response_entity.json(indent=2))

    return cls
