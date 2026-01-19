from gemsModules.common.main_api_notices import Notices
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


# TODO: this likely can be a common task that all response managers can use.
def execute(response_manager, clear_payloads=True):
    request_aaop_list = response_manager.aaop_tree_pair.input_tree.make_linear_list()
    response_aaop_list = response_manager.aaop_tree_pair.output_tree.make_linear_list()
    log.debug(
        "the request aaop list is: %s\nthe response aaop list is: %s",
        request_aaop_list,
        response_aaop_list,
    )
    for aaop in request_aaop_list:
        this_service = aaop.The_AAO.copy(deep=True)

        # Prevent the service from carrying over any payloads from the request to the response json.
        # As payloads are uploaded, there is no reason to return them to the uploader, but we still return
        # the Resource's metadata, which can be used to reconstruct the request from the response.
        if clear_payloads:
            this_service.inputs.resources.clear_payloads()

        this_service.myUuid = aaop.ID_String
        response_manager.response_entity.services.add_service(
            key_string=aaop.Dictionary_Name, service=this_service
        )
    for aaop in response_aaop_list:
        this_response = aaop.The_AAO.copy(deep=True)
        this_response.myUuid = aaop.ID_String
        this_response.notices = Notices()
        response_manager.response_entity.responses.add_response(
            key_string=aaop.Dictionary_Name, response=this_response
        )

    log.debug("the response entity is: ")
    log.debug(response_manager.response_entity.json(indent=2))

    return response_manager
