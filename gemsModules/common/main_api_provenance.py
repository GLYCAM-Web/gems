#!/usr/bin/env python3
import os
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class HostContext(BaseModel):
    name: str = ""
    timestamp: str = ""
    secure_inputs_path: Optional[str] = ""
    filesystem_path: Optional[str] = ""
    supported_contexts: List[str] = []
    options: Dict[str, str] = {}


class Provenance(BaseModel):
    initial_receiver: HostContext = Field(default_factory=HostContext)
    execution_host: Optional[HostContext] = Field(default_factory=HostContext)


def translate_path_prefix(path_str: Optional[str], from_prefix: Optional[str], to_prefix: Optional[str]) -> Optional[str]:
    """
    Translate path prefix from from_prefix to to_prefix.
    Ensures safe prefix boundary checking (directory boundary).
    """
    if not path_str or not from_prefix or not to_prefix or from_prefix == to_prefix:
        return path_str

    from_norm = os.path.normpath(from_prefix)
    to_norm = os.path.normpath(to_prefix)
    p_norm = os.path.normpath(path_str)

    if p_norm == from_norm:
        return to_norm

    from_norm_sep = from_norm if from_norm.endswith(os.sep) else from_norm + os.sep
    if p_norm.startswith(from_norm_sep):
        rel = os.path.relpath(p_norm, from_norm)
        return os.path.join(to_norm, rel)

    return path_str


def translate_request_paths(
    data: dict,
    from_secure: Optional[str],
    to_secure: Optional[str],
    from_fs: Optional[str],
    to_fs: Optional[str],
) -> dict:
    """
    Translates input paths in a request dictionary from initial receiver to execution host.
    """
    if not isinstance(data, dict):
        return data

    def _xlate(val: str) -> str:
        if not isinstance(val, str):
            return val
        res = translate_path_prefix(val, from_secure, to_secure)
        res = translate_path_prefix(res, from_fs, to_fs)
        return res

    # 1. Translate resources and known path inputs in entity.services
    entity = data.get("entity")
    if isinstance(entity, dict):
        services = entity.get("services")
        if isinstance(services, dict):
            for svc_name, svc in services.items():
                if not isinstance(svc, dict):
                    continue
                inputs = svc.get("inputs")
                if isinstance(inputs, dict):
                    # Resources
                    resources = inputs.get("resources")
                    if isinstance(resources, list):
                        for r in resources:
                            if isinstance(r, dict):
                                loc = r.get("locationType")
                                if loc in ("filesystem-path-unix", "File", "Unset", None):
                                    payload = r.get("payload")
                                    if isinstance(payload, str):
                                        r["payload"] = _xlate(payload)
                    # Known specific fields
                    for field in ("antibody_path", "ligand_path", "inputFilePath", "outputFilePath", "pdb_filename"):
                        if field in inputs and isinstance(inputs[field], str):
                            inputs[field] = _xlate(inputs[field])

    # 2. Translate project paths if project is present
    project = data.get("project")
    if isinstance(project, dict):
        for field in ("uploads_path", "secure_inputs_path"):
            if field in project and isinstance(project[field], str):
                project[field] = translate_path_prefix(project[field], from_secure, to_secure)
        for field in ("filesystem_path", "service_dir", "project_dir", "logs_dir"):
            if field in project and isinstance(project[field], str):
                project[field] = translate_path_prefix(project[field], from_fs, to_fs)

    return data


def translate_response_paths(
    data: dict,
    from_fs: Optional[str],
    to_fs: Optional[str],
    from_secure: Optional[str],
    to_secure: Optional[str],
) -> dict:
    """
    Translates output paths in a response dictionary from execution host back to initial receiver.
    """
    if not isinstance(data, dict):
        return data

    def _xlate(val: str) -> str:
        if not isinstance(val, str):
            return val
        res = translate_path_prefix(val, from_fs, to_fs)
        res = translate_path_prefix(res, from_secure, to_secure)
        return res

    # 1. Translate resources and output fields in entity.services / entity.responses
    entity = data.get("entity")
    if isinstance(entity, dict):
        for container_key in ("services", "responses"):
            container = entity.get(container_key)
            if isinstance(container, dict):
                for item_name, item in container.items():
                    if not isinstance(item, dict):
                        continue
                    # Check outputs
                    outputs = item.get("outputs")
                    if isinstance(outputs, dict):
                        resources = outputs.get("resources")
                        if isinstance(resources, list):
                            for r in resources:
                                if isinstance(r, dict):
                                    loc = r.get("locationType")
                                    if loc in ("filesystem-path-unix", "File", "Unset", None):
                                        payload = r.get("payload")
                                        if isinstance(payload, str):
                                            r["payload"] = _xlate(payload)
                        # Specific output fields
                        for k, v in outputs.items():
                            if isinstance(v, str) and (from_fs and from_fs in v or from_secure and from_secure in v):
                                outputs[k] = _xlate(v)

    # 2. Translate project paths
    project = data.get("project")
    if isinstance(project, dict):
        for field in ("filesystem_path", "service_dir", "project_dir", "logs_dir"):
            if field in project and isinstance(project[field], str):
                project[field] = translate_path_prefix(project[field], from_fs, to_fs)
        for field in ("uploads_path", "secure_inputs_path"):
            if field in project and isinstance(project[field], str):
                project[field] = translate_path_prefix(project[field], from_secure, to_secure)

    return data
