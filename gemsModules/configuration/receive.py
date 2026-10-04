#!/usr/bin/env python3
import json
import os
import sys

from gemsModules.systemoperations.environment_ops import find_instance_config
from gemsModules.configuration.control_script import export_host
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Configuration was called as an entity. Processing.")
    try:
        req_dict = json.loads(incomingString)
    except Exception as e:
        log.error(f"Failed to parse incoming JSON string: {e}")
        return json.dumps({
            "entity": {
                "type": "Configuration",
                "responses": {
                    "Error": {"message": f"Invalid JSON string: {str(e)}"}
                }
            }
        })

    entity_info = req_dict.get("entity", {})
    requests = entity_info.get("requests", {})
    services = entity_info.get("services", {})

    target = "localhost"
    if "ExportHost" in requests:
        target = requests["ExportHost"].get("inputs", {}).get("target", "localhost")
    elif "ExportHost" in services:
        target = services["ExportHost"].get("inputs", {}).get("target", "localhost")

    ic_path = find_instance_config()
    try:
        export_json_str = export_host(ic_path, target)
        export_obj = json.loads(export_json_str)
        response_data = {
            "entity": {
                "type": "Configuration",
                "responses": {
                    "ExportHost": {
                        "type": "ExportHost",
                        "outputs": {
                            "configuration": export_obj
                        }
                    }
                }
            }
        }
        return json.dumps(response_data)
    except Exception as e:
        log.error(f"Error exporting host configuration for target '{target}': {e}")
        return json.dumps({
            "entity": {
                "type": "Configuration",
                "responses": {
                    "ExportHost": {
                        "type": "ExportHost",
                        "outputs": {
                            "error": str(e)
                        }
                    }
                }
            }
        })


if __name__ == "__main__":
    test_req = {
        "entity": {
            "type": "Configuration",
            "requests": {
                "ExportHost": {
                    "type": "ExportHost",
                    "inputs": {"target": "localhost"}
                }
            }
        }
    }
    print(receive(json.dumps(test_req)))
