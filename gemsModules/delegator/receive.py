#!/usr/bin/env python3
import json
from datetime import datetime

from gemsModules.logging.logger import Set_Up_Logging
from gemsModules.configuration.main_api import session_instance_config
from gemsModules.common.main_api_provenance import (
    normalize_storage_root,
    translate_request_paths,
    translate_response_paths,
)
from gemsModules.delegator.main_settings import WhoIAm

log = Set_Up_Logging(__name__)


def process(incomingString: str) -> str:
    log.info("Delegator was called as an entity.  Processing.")
    from gemsModules.delegator.json_string_manager import Delegator_Json_String_Manager
    delegator_string_manager = Delegator_Json_String_Manager()
    delegator_string_manager_error_response = delegator_string_manager.process(
        incoming_string=incomingString
    )
    if delegator_string_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return delegator_string_manager_error_response
    log.debug("The incoming string is valid")
    return delegator_string_manager.transaction.get_outgoing_string()


def receive(incomingString: str) -> str:
    log.info("Delegator's receive was called")

    tmp_dict = json.loads(incomingString)
    requested_entity = tmp_dict["entity"]["type"]
    log.debug("The requested entity is : " + requested_entity)
    local_host_name = session_instance_config.get_localhost_hostName()
    localhost = session_instance_config.get_localhost()
    now_str = str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    # Resolve local paths for the requested entity
    local_sec_path = None
    local_fs_path = None
    try:
        local_sec_path = session_instance_config.get_secure_inputs_path_by_service_ID(serviceID=requested_entity)
        if local_sec_path:
            local_sec_path = normalize_storage_root(local_sec_path)
    except Exception:
        pass
    try:
        local_fs_path = session_instance_config.get_filesystem_path_by_service_ID(serviceID=requested_entity)
        if local_fs_path:
            local_fs_path = normalize_storage_root(local_fs_path)
    except Exception:
        pass

    local_contexts = []
    if localhost and hasattr(localhost, "execution_environments") and localhost.execution_environments:
        local_contexts = [str(ctx) for ctx in localhost.execution_environments]

    # Setup or retrieve provenance
    prov_dict = tmp_dict.get("provenance")
    if not isinstance(prov_dict, dict):
        prov_dict = {}

    init_rec = prov_dict.get("initial_receiver")
    if not isinstance(init_rec, dict) or not init_rec.get("name"):
        init_rec_name = tmp_dict.get("initial_receiver") or local_host_name
        init_rec_ts = tmp_dict.get("initiation_timestamp") or now_str
        init_rec_sec = local_sec_path or ""
        init_rec_fs = local_fs_path or ""
        prov_dict["initial_receiver"] = {
            "name": init_rec_name,
            "timestamp": init_rec_ts,
            "secure_inputs_path": init_rec_sec,
            "filesystem_path": init_rec_fs,
            "supported_contexts": local_contexts,
            "options": {},
        }
        tmp_dict["initial_receiver"] = init_rec_name
        tmp_dict["initiation_timestamp"] = init_rec_ts
    else:
        if "initial_receiver" not in tmp_dict or not tmp_dict["initial_receiver"]:
            tmp_dict["initial_receiver"] = init_rec.get("name", "")
        if "initiation_timestamp" not in tmp_dict or not tmp_dict["initiation_timestamp"]:
            tmp_dict["initiation_timestamp"] = init_rec.get("timestamp", now_str)

    # Set execution host in provenance
    prov_dict["execution_host"] = {
        "name": local_host_name,
        "timestamp": now_str,
        "secure_inputs_path": local_sec_path or "",
        "filesystem_path": local_fs_path or "",
        "supported_contexts": local_contexts,
        "options": {},
    }
    tmp_dict["execution_host"] = local_host_name
    tmp_dict["provenance"] = prov_dict

    # Translate paths forward (initial_receiver -> execution_host)
    from_sec = prov_dict["initial_receiver"].get("secure_inputs_path")
    to_sec = prov_dict["execution_host"].get("secure_inputs_path")
    from_fs = prov_dict["initial_receiver"].get("filesystem_path")
    to_fs = prov_dict["execution_host"].get("filesystem_path")

    # Fallback: if from_sec is missing but to_sec is set and paths start with /website/uploads
    if not from_sec and to_sec:
        from gemsModules.project import settings as project_settings
        from_sec = getattr(project_settings, "default_website_filesystem_uploads_path", "/website/uploads/")

    tmp_dict = translate_request_paths(
        tmp_dict,
        from_secure=from_sec,
        to_secure=to_sec,
        from_fs=from_fs,
        to_fs=to_fs,
    )

    incoming_string = json.dumps(tmp_dict)

    # Dispatch to delegator or target entity
    if requested_entity == WhoIAm:
        log.info("The requested entity is the delegator. Processing.")
        raw_response = process(incoming_string)
    else:
        log.info("The requested entity is NOT delegator. Redirecting")
        log.debug("Delegating incoming string to entity: " + requested_entity)
        from gemsModules.delegator.redirector_settings import module_loader
        entity_module = module_loader.get_module_attr(requested_entity)
        raw_response = entity_module(incoming_string)

    # Translate paths in reverse (execution_host -> initial_receiver)
    try:
        resp_dict = json.loads(raw_response)
        resp_dict = translate_response_paths(
            resp_dict,
            from_fs=to_fs,
            to_fs=from_fs,
            from_secure=to_sec,
            to_secure=from_sec,
        )
        if "provenance" not in resp_dict:
            resp_dict["provenance"] = prov_dict
        else:
            resp_dict["provenance"]["execution_host"] = prov_dict["execution_host"]

        resp_dict["execution_host"] = local_host_name
        if "initial_receiver" not in resp_dict:
            resp_dict["initial_receiver"] = prov_dict["initial_receiver"]["name"]
        if "initiation_timestamp" not in resp_dict:
            resp_dict["initiation_timestamp"] = prov_dict["initial_receiver"]["timestamp"]

        pretty = False
        if resp_dict.get("prettyPrint") or resp_dict.get("entity", {}).get("procedural_options", {}).get("pretty_print"):
            pretty = True

        return json.dumps(resp_dict, indent=2 if pretty else None)
    except Exception as err:
        log.debug(f"Could not reverse-translate response: {err}")
        return raw_response
