#!/usr/bin/env python3
import sys
import os
import json
import copy
import datetime
from typing import Dict, List, Any, Optional

# Adjust paths if run as script
GEMSHOME = os.environ.get("GEMSHOME", "")
if GEMSHOME not in sys.path:
    sys.path.append(GEMSHOME)

from gemsModules.configuration.main_api import (
    SupportedEntities,
    ExecutionEnvironments,
    WebsiteEnvironments,
    BatchComputingResources,
    Host,
    InstanceConfig
)
from gemsModules.configuration.resource_management_api import (
    Resource_Specific_Information_Registry,
    Slurm_Specific_Information
)

def print_tui_help():
    summary = """
=== TUI Questionnaire Summary ===
This TUI guides you through creating a GEMS Instance Configuration (IC) file.
The Q/A process collects the following information:
1. Basic Setup:
   - Output configuration filename (default: instance_config.json)
   - Entities to delegate from the Local Host (e.g., AD, BC, CB, GM, GP, GR, MD, PDB)
   - Local filesystem paths for each delegatable Entity
   - Secure inputs paths for each delegatable Entity
2. Local Host Setup:
   - Host Name (default: Glycon)
   - Host Address (e.g., localhost, 127.0.0.1, or remote address)
   - Port (if contacted by other hosts)
   - Execution Environments supported (e.g., Standalone, Batch, Swarm, Docker)
   - Website Environment (if serving a website, e.g., DevEnv, Actual, Test)
   - Served Entities (entities that can run locally on this host)
   - Scheduler details (Slurm or None)
     * If Slurm is chosen: BatchComputingResources (partition, nodes, cores, etc.) and
       Slurm-specific options (use_gres_for_gpus, cpu_hardware_equivalent)
3. Remote Host Setup (Optional):
   - Prompt to manually add remote hosts or exit.
"""
    print(summary.strip())

def ask_question(prompt: str, default: str = "", help_text: str = "") -> str:
    while True:
        try:
            val = input(f"{prompt} ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting TUI.")
            sys.exit(1)
            
        if val == "?":
            if help_text:
                print(help_text)
            else:
                print("No help available for this prompt.")
            continue
            
        if not val:
            return default
        return val

def ask_list_question(prompt: str, valid_values: List[str], default: List[str] = None, help_text: str = "") -> List[str]:
    while True:
        val = ask_question(prompt, default=" ".join(default) if default else "", help_text=help_text)
        parts = [p for p in val.replace(",", " ").split() if p]
        
        # Check invalid values
        invalid = [p for p in parts if p not in valid_values]
        if invalid:
            print(f"Invalid entries: {invalid}. Allowed entries: {valid_values}")
            continue
        return parts

def run_tui() -> Dict[str, Any]:
    now_str = datetime.datetime.now().isoformat()
    print(f"Beginning a new Instance Configuration file on {now_str}.\n")
    print("At any prompt, enter '?' for help.\n")
    print("-" * 42)
    print("Basic Setup")
    print("-" * 42)

    ic_filename = ask_question('Instance configuration file name ["instance_config.json"] :', 
                               default="instance_config.json",
                               help_text="The name of the file to save the Instance Configuration to.")

    print("\nFirst we must gather some local data storage information\n")
    
    entity_vals = SupportedEntities.get_value_list()
    entity_help = "Available Entities and descriptions:\n" + "\n".join(
        [f"  {val}: {SupportedEntities(val).description}" for val in entity_vals]
    )
    
    delegated_entities = ask_list_question(
        f"Enter the list of Entities that can be delegated from the Local Host (space separated)\n"
        f"  Note that this is NOT the list of Entities that can run on this host.\n"
        f"  It is the list of all entities considered, including those sent to remote hosts.\n"
        f"  {entity_vals} :",
        valid_values=entity_vals,
        help_text=entity_help
    )

    filesystem_paths = {}
    print("\nFor each delegatable Entity, please provide a local filesystem path")
    for entity in delegated_entities:
        path = ask_question(
            f"  {entity} [] :",
            default="",
            help_text="Local filesystem path for this Entity's outputs. If submitting to a cluster, where to drop files locally."
        )
        if path:
            filesystem_paths[entity] = path

    secure_inputs_paths = {}
    print("\nFor each delegatable Entity, please provide a local secure inputs path")
    for entity in delegated_entities:
        path = ask_question(
            f"  {entity} [] :",
            default="",
            help_text="Local secured and sanitized space for storing uploads/inputs."
        )
        if path:
            secure_inputs_paths[entity] = path

    hosts_list = []

    def setup_host(is_local: bool) -> Dict[str, Any]:
        h_data = {}
        h_data["is_localhost"] = "True" if is_local else "False"
        
        name_prompt = 'Please enter the name by which this host is known ["Glycon"] :' if is_local else 'Please enter the name by which this remote host is known :'
        h_data["name"] = ask_question(name_prompt, default="Glycon" if is_local else "", help_text="Whatever the humans call this machine.")
        
        addr_default = "localhost" if is_local else ""
        addr_prompt = 'Please enter the host address. If this host is to be contacted by other hosts, enter a remote address, otherwise \'localhost\' is sufficient ["localhost"] :' if is_local else 'Please enter the remote host address (IP or domain name) :'
        h_data["address"] = ask_question(addr_prompt, default=addr_default, help_text="Networking contact information for the host.")
        
        h_data["port"] = ask_question('Please enter the port address if this host is to be contacted by other hosts [] :', default="", help_text="The gRPC port that should be used to connect to this GEMS instance.")
        if not h_data["port"]:
            h_data["port"] = None

        env_vals = ExecutionEnvironments.get_value_list()
        env_help = "Available Execution Environments:\n" + "\n".join(
            [f"  {val}: {ExecutionEnvironments(val).description}" for val in env_vals]
        )
        envs = ask_list_question(
            'Please enter the list of execution environments supported by this host ["Standalone"] :',
            valid_values=env_vals,
            default=["Standalone"],
            help_text=env_help
        )
        h_data["execution_environments"] = envs

        h_data["website_environments"] = None
        if "Website" in envs:
            web_vals = WebsiteEnvironments.get_value_list()
            web_help = "Available Website Environments:\n" + "\n".join(
                [f"  {val}: {WebsiteEnvironments(val).description}" for val in web_vals]
            )
            web_envs = ask_list_question(
                'If this host serves a website, please enter the website environment that it will serve [DevEnv] :',
                valid_values=web_vals,
                default=["DevEnv"],
                help_text=web_help
            )
            h_data["website_environments"] = web_envs

        served_entities = ask_list_question(
            'Enter the list of Entities that can be Served from the Local Host (space separated)\n'
            '  Note that this IS the list of Entities that can run on this host.\n'
            f'  {entity_vals} :',
            valid_values=entity_vals,
            help_text=entity_help
        )
        h_data["entities_available"] = served_entities

        scheduler_val = ask_question(
            'If this host uses a resource scheduler, please give the type [None]\n'
            '  Note that the only possible options right now are "Slurm" and "None" :',
            default="None",
            help_text="The type of scheduler used on this host, e.g., 'slurm'."
        )
        
        if scheduler_val.lower() == "none" or not scheduler_val:
            h_data["scheduler"] = None
            h_data["batch_computing_resources"] = None
            h_data["resource_specific_information"] = None
        else:
            h_data["scheduler"] = scheduler_val.lower()
            print("\nFor the resource, please fill in the following information.")
            print("If you are unsure of the answers, give a dummy answer and contact the staff for the resource.")
            
            # BatchComputingResources Q/A
            res_data = {}
            res_data["partition"] = ask_question("  partition [None] :", default="", help_text="The partition or queue.")
            res_data["supported_entities"] = ask_list_question(
                "  supported_entities (space separated list of Entities served by this partition) :",
                valid_values=entity_vals,
                help_text="The list of Entities that this partition supports."
            )
            res_data["max_nodes_per_job"] = ask_question("  max_nodes_per_job [None] :", default="", help_text="Maximum nodes per job.")
            res_data["max_cores_per_node"] = ask_question("  max_cores_per_node [None] :", default="", help_text="Maximum cores per node.")
            res_data["max_threads_per_node"] = ask_question("  max_threads_per_node [None] :", default="", help_text="Maximum threads per node.")
            res_data["max_gpus_per_node"] = ask_question("  max_gpus_per_node [None] :", default="", help_text="Maximum gpus per node.")
            res_data["max_cpus_per_gpu"] = ask_question("  max_cpus_per_gpu [1] :", default="1", help_text="Maximum cpus per gpu.")
            res_data["max_time_limit"] = ask_question("  max_time_limit [None] :", default="", help_text="ISO 8601 duration string, e.g., P2DT16H30M.")
            
            # Clean up empty strings
            cleaned_res = {k: (v if v != "" else None) for k, v in res_data.items()}
            h_data["batch_computing_resources"] = [cleaned_res]
            
            # Scheduler specific info
            if h_data["scheduler"] == "slurm":
                slurm_data = {}
                slurm_data["use_gres_for_gpus"] = ask_question("  use_gres_for_gpus [True] :", default="True", help_text="Should GPUs be reserved as --gpus or --gres?")
                slurm_data["cpu_hardware_equivalent"] = ask_question("  cpu_hardware_equivalent [core] :", default="core", help_text="Is a CPU considered to be a core or a thread?")
                h_data["resource_specific_information"] = slurm_data
            else:
                h_data["resource_specific_information"] = None
                
        return h_data

    print("\n" + "-" * 42)
    print("Local Host Setup")
    print("-" * 42)
    local_host = setup_host(is_local=True)
    hosts_list.append(local_host)

    print("\n" + "-" * 42)
    print("Remote Host Setup")
    print("-" * 42)
    while True:
        ans = ask_question("Do you want to enter remote host information? [No] :", default="No", help_text="Enter remote host details manually.")
        if ans.lower() in ("no", "n"):
            break
        elif ans.lower() in ("yes", "y"):
            remote_host = setup_host(is_local=False)
            hosts_list.append(remote_host)
        else:
            print("Please enter 'yes' or 'no'.")

    ic_dict = {
        "date": now_str,
        "hosts": hosts_list,
        "filesystem_paths": filesystem_paths,
        "secure_inputs_paths": secure_inputs_paths
    }
    
    return ic_filename, ic_dict

def generate_from_tui():
    ic_filename, ic_dict = run_tui()
    # Validate with Pydantic
    try:
        InstanceConfig(**ic_dict)
    except Exception as e:
        print(f"Validation failed for generated config: {e}", file=sys.stderr)
        sys.exit(1)
        
    with open(ic_filename, "w") as f:
        json.dump(ic_dict, f, indent=2)
    
    # Mark read-only where possible
    try:
        os.chmod(ic_filename, 0o444)
        print(f"Successfully generated config file '{ic_filename}' (marked read-only).")
    except Exception:
        print(f"Successfully generated config file '{ic_filename}'.")

def export_host(ic_path: str, host_name: str, to_file: str = None) -> str:
    if not os.path.exists(ic_path):
        print(f"Error: configuration file '{ic_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    with open(ic_path) as f:
        config = json.load(f)
        
    # We find the host
    hosts_data = config.get("hosts", [])
    target_host = None

    if isinstance(hosts_data, dict):
        if host_name.lower() == "localhost":
            for name, h in hosts_data.items():
                if isinstance(h, dict) and str(h.get("is_localhost", "False")).lower() == "true":
                    target_host = h.copy()
                    if "name" not in target_host:
                        target_host["name"] = name
                    break
        else:
            for name, h in hosts_data.items():
                if isinstance(h, dict) and (name == host_name or h.get("name") == host_name):
                    target_host = h.copy()
                    if "name" not in target_host:
                        target_host["name"] = name
                    break
    elif isinstance(hosts_data, list):
        if host_name.lower() == "localhost":
            for h in hosts_data:
                if isinstance(h, dict) and str(h.get("is_localhost", "False")).lower() == "true":
                    target_host = h.copy()
                    break
        else:
            for h in hosts_data:
                if isinstance(h, dict) and h.get("name") == host_name:
                    target_host = h.copy()
                    break
                
    if not target_host:
        print(f"Error: Host '{host_name}' not found.", file=sys.stderr)
        sys.exit(1)
        
    # Create the export json
    export_data = {
        "hosts": [target_host],
        "filesystem_paths": config.get("filesystem_paths", {}),
        "secure_inputs_paths": config.get("secure_inputs_paths", {})
    }
    
    out_str = json.dumps(export_data, indent=2)
    if to_file:
        with open(to_file, "w") as f:
            f.write(out_str)
        print(f"Exported host '{host_name}' to '{to_file}'.")
    return out_str

def import_host(ic_path: str, remote_ic_path: str, out_ic_path: str = None):
    if not os.path.exists(ic_path):
        print(f"Error: Local configuration file '{ic_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(remote_ic_path):
        print(f"Error: Remote configuration file '{remote_ic_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
        
    with open(ic_path) as f:
        local_config = json.load(f)
    with open(remote_ic_path) as f:
        remote_config = json.load(f)
        
    # Merge hosts
    local_hosts_data = local_config.get("hosts", [])
    local_hosts = {}
    if isinstance(local_hosts_data, dict):
        for name, h in local_hosts_data.items():
            if isinstance(h, dict):
                h_copy = h.copy()
                if "name" not in h_copy:
                    h_copy["name"] = name
                local_hosts[h_copy["name"]] = h_copy
    elif isinstance(local_hosts_data, list):
        for h in local_hosts_data:
            if isinstance(h, dict) and "name" in h:
                local_hosts[h["name"]] = h

    remote_hosts_data = remote_config.get("hosts", [])
    remote_hosts = []
    if isinstance(remote_hosts_data, dict):
        for name, h in remote_hosts_data.items():
            if isinstance(h, dict):
                h_copy = h.copy()
                if "name" not in h_copy:
                    h_copy["name"] = name
                remote_hosts.append(h_copy)
    elif isinstance(remote_hosts_data, list):
        remote_hosts = remote_hosts_data
    
    for rh in remote_hosts:
        if not isinstance(rh, dict):
            continue
        # Remote hosts should never be marked as localhost in local IC
        rh_copy = rh.copy()
        rh_copy["is_localhost"] = "False"
        name = rh_copy.get("name", "UnknownRemote")
        if name in local_hosts:
            print(f"Overwriting host details for '{name}' with imported information.")
        local_hosts[name] = rh_copy
        
    local_config["hosts"] = list(local_hosts.values())
    
    # Merge paths
    for p_type in ("filesystem_paths", "secure_inputs_paths"):
        if p_type not in local_config:
            local_config[p_type] = {}
        for k, v in remote_config.get(p_type, {}).items():
            if k not in local_config[p_type]:
                local_config[p_type][k] = v
                
    local_config["date"] = datetime.datetime.now().isoformat()
    
    # Validate with Pydantic
    try:
        InstanceConfig(**local_config)
    except Exception as e:
        print(f"Validation failed for merged config: {e}", file=sys.stderr)
        sys.exit(1)
        
    dest_path = out_ic_path if out_ic_path else ic_path
    
    # Check if dest is writeable/read-only
    if os.path.exists(dest_path):
        try:
            os.chmod(dest_path, 0o644)
        except Exception:
            pass
            
    with open(dest_path, "w") as f:
        json.dump(local_config, f, indent=2)
        
    try:
        os.chmod(dest_path, 0o444)
    except Exception:
        pass
        
    print(f"Import complete. Written to '{dest_path}'.")


class _SafeFormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def _format_templates(obj: Any, context: Dict[str, Any]) -> Any:
    """Recursively format string values in dicts/lists using context."""
    if isinstance(obj, str):
        return obj.format_map(_SafeFormatDict(context))
    if isinstance(obj, list):
        return [_format_templates(item, context) for item in obj]
    if isinstance(obj, dict):
        return {k: _format_templates(v, context) for k, v in obj.items()}
    return obj


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge override dict into a copy of base dict."""
    result = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result


def _normalize_hosts_list(hosts_data: Any) -> List[Dict[str, Any]]:
    """Normalize hosts from either dict or list format into a list of host dicts."""
    hosts = []
    if isinstance(hosts_data, dict):
        for name, h in hosts_data.items():
            if isinstance(h, dict):
                h_copy = copy.deepcopy(h)
                if "name" not in h_copy:
                    h_copy["name"] = name
                hosts.append(h_copy)
    elif isinstance(hosts_data, list):
        for h in hosts_data:
            if isinstance(h, dict):
                hosts.append(copy.deepcopy(h))
    return hosts


def _write_ic_file(dest_path: str, ic_dict: Dict[str, Any], minify: bool = False) -> None:
    """Validate ic_dict with InstanceConfig and write it to dest_path (read-only 0o444)."""
    try:
        InstanceConfig(**ic_dict)
    except Exception as e:
        print(f"Validation failed for '{dest_path}': {e}", file=sys.stderr)
        sys.exit(1)

    parent = os.path.dirname(os.path.abspath(dest_path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    if os.path.exists(dest_path):
        try:
            os.chmod(dest_path, 0o644)
        except Exception:
            pass

    indent = None if minify else 2
    with open(dest_path, "w") as f:
        json.dump(ic_dict, f, indent=indent)

    try:
        os.chmod(dest_path, 0o444)
    except Exception:
        pass


def _expand_entity_paths(
    template: Optional[str],
    entities: List[str],
    context: Dict[str, Any],
) -> Dict[str, str]:
    """Expand a path template (e.g. '/scratch/{id}/{entity}') across entities."""
    if not template:
        return {}
    has_entity_placeholder = "{entity}" in template
    paths = {}
    for ent in entities:
        ctx = dict(context)
        ctx["entity"] = ent
        formatted = template.format_map(_SafeFormatDict(ctx))
        if not has_entity_placeholder:
            formatted = os.path.join(formatted, ent)
        paths[ent] = formatted
    return paths


def _filter_by_entities(
    host_dict: Dict[str, Any],
    fs_paths: Dict[str, str],
    sec_paths: Dict[str, str],
    entities: List[str],
) -> None:
    """Scope host_dict, batch_computing_resources, and path dicts to the given entities."""
    entity_set = set(entities)
    host_dict["entities_available"] = list(entities)

    bcr = host_dict.get("batch_computing_resources")
    if isinstance(bcr, list):
        filtered_bcr = []
        for part in bcr:
            if not isinstance(part, dict):
                continue
            part_copy = copy.deepcopy(part)
            supported = part_copy.get("supported_entities")
            if supported is not None:
                kept = [e for e in supported if e in entity_set]
                if not kept:
                    continue
                part_copy["supported_entities"] = kept
            filtered_bcr.append(part_copy)
        host_dict["batch_computing_resources"] = filtered_bcr

    for path_dict in (fs_paths, sec_paths):
        for k in list(path_dict.keys()):
            if k not in entity_set:
                del path_dict[k]


def generate_from_matrix(
    matrix_path: str,
    output_dir: Optional[str] = None,
    minify: bool = False,
) -> List[str]:
    """Generate a family of Instance Config files from a cluster matrix JSON file."""
    if not os.path.exists(matrix_path):
        print(f"Error: Matrix file '{matrix_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(matrix_path) as f:
        matrix = json.load(f)

    base = matrix.get("base", {})
    variants = matrix.get("variants", [])
    if not isinstance(variants, list) or not variants:
        print("Error: Matrix JSON must contain a non-empty 'variants' list.", file=sys.stderr)
        sys.exit(1)

    HOST_FIELDS = {
        "name",
        "address",
        "port",
        "is_localhost",
        "scheduler",
        "execution_environments",
        "website_environments",
        "entities_available",
        "batch_computing_resources",
        "resource_specific_information",
        "entity_resources",
    }

    base_host = {k: copy.deepcopy(v) for k, v in base.items() if k in HOST_FIELDS}
    base_host.setdefault("is_localhost", "True")

    generated_files = []
    now_str = datetime.datetime.now().isoformat()

    for idx, var in enumerate(variants):
        if not isinstance(var, dict):
            print(f"Error: Variant at index {idx} must be a JSON object.", file=sys.stderr)
            sys.exit(1)

        var_id = var.get("id", f"variant{idx}")
        ctx: Dict[str, Any] = {"id": var_id, "env": var.get("env", var_id)}
        for k, v in var.items():
            if isinstance(v, (str, int, float)):
                ctx[k] = v

        # Resolve host name
        base_name = base.get("name", "Glycon")
        if "name" in var:
            host_name = _format_templates(var["name"], ctx)
        elif "name_template" in base:
            host_name = _format_templates(base["name_template"], ctx)
        elif "{" in base_name:
            host_name = _format_templates(base_name, ctx)
        elif "id" in var:
            host_name = f"{base_name}-{var_id}"
        else:
            host_name = base_name
        ctx["name"] = host_name

        var_host_overrides = {k: v for k, v in var.items() if k in HOST_FIELDS}
        if "entities" in var and "entities_available" not in var_host_overrides:
            var_host_overrides["entities_available"] = var["entities"]

        local_host = _deep_merge(base_host, var_host_overrides)
        local_host["name"] = host_name
        local_host = _format_templates(local_host, ctx)

        entities = local_host.get("entities_available") or []

        # Build filesystem_paths and secure_inputs_paths
        fs_template = var.get("filesystem_path_template", base.get("filesystem_path_template"))
        sec_template = var.get("secure_inputs_path_template", base.get("secure_inputs_path_template"))

        fs_paths = _expand_entity_paths(fs_template, entities, ctx)
        sec_paths = _expand_entity_paths(sec_template, entities, ctx)

        explicit_fs = _deep_merge(base.get("filesystem_paths", {}), var.get("filesystem_paths", {}))
        explicit_sec = _deep_merge(base.get("secure_inputs_paths", {}), var.get("secure_inputs_paths", {}))
        fs_paths.update(_format_templates(explicit_fs, ctx))
        sec_paths.update(_format_templates(explicit_sec, ctx))

        if entities:
            _filter_by_entities(local_host, fs_paths, sec_paths, entities)

        hosts = [local_host]
        remote_hosts = var.get("remote_hosts", base.get("remote_hosts", []))
        if isinstance(remote_hosts, list):
            for rh in remote_hosts:
                rh_copy = _format_templates(copy.deepcopy(rh), ctx)
                rh_copy["is_localhost"] = "False"
                hosts.append(rh_copy)

        ic_dict: Dict[str, Any] = {
            "date": now_str,
            "hosts": hosts,
            "filesystem_paths": fs_paths,
            "secure_inputs_paths": sec_paths,
        }

        out_name = var.get("output") or f"instance_config.{var_id}.json"
        dest_path = os.path.join(output_dir, out_name) if output_dir else out_name

        _write_ic_file(dest_path, ic_dict, minify=minify)
        generated_files.append(dest_path)
        print(f"Generated '{dest_path}' (host='{host_name}', port={local_host.get('port')}, entities={entities})")

    return generated_files


def _apply_dotted_set(target: Dict[str, Any], key_path: str, raw_value: str) -> None:
    """Set a dotted key path (e.g. 'resource_specific_information.use_gres_for_gpus=False') on target."""
    parts = key_path.split(".")
    cur = target
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    # Try JSON parse for lists/dicts/null, fallback to raw string
    val: Any = raw_value
    if raw_value.lower() == "none" or raw_value.lower() == "null":
        val = None
    elif raw_value.startswith("[") or raw_value.startswith("{"):
        try:
            val = json.loads(raw_value)
        except Exception:
            val = raw_value
    cur[parts[-1]] = val


def clone_ic(
    source_path: str,
    dest_path: str,
    name: Optional[str] = None,
    address: Optional[str] = None,
    port: Optional[str] = None,
    entities: Optional[List[str]] = None,
    fs_template: Optional[str] = None,
    inputs_template: Optional[str] = None,
    website_envs: Optional[List[str]] = None,
    exec_envs: Optional[List[str]] = None,
    aad2_home: Optional[str] = None,
    sets: Optional[List[str]] = None,
    drop_remote_hosts: bool = False,
    minify: bool = False,
) -> str:
    """Clone an existing Instance Config file with targeted overrides."""
    if not os.path.exists(source_path):
        print(f"Error: Source configuration file '{source_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(source_path) as f:
        src_data = json.load(f)

    hosts = _normalize_hosts_list(src_data.get("hosts", []))
    if not hosts:
        print(f"Error: No hosts found in '{source_path}'.", file=sys.stderr)
        sys.exit(1)

    local_idx = None
    for i, h in enumerate(hosts):
        if str(h.get("is_localhost", "False")).lower() == "true":
            local_idx = i
            break
    if local_idx is None:
        local_idx = 0
        hosts[0]["is_localhost"] = "True"

    local_host = hosts[local_idx]

    if name is not None:
        local_host["name"] = name
    if address is not None:
        local_host["address"] = address
    if port is not None:
        local_host["port"] = None if port.lower() in ("none", "null", "") else port
    if website_envs is not None:
        local_host["website_environments"] = website_envs
    if exec_envs is not None:
        local_host["execution_environments"] = exec_envs

    if aad2_home is not None:
        rsi = local_host.setdefault("resource_specific_information", {})
        if not isinstance(rsi, dict):
            rsi = {}
            local_host["resource_specific_information"] = rsi
        aad2_cfg = rsi.setdefault("aad2_configuration", {})
        if not isinstance(aad2_cfg, dict):
            aad2_cfg = {}
            rsi["aad2_configuration"] = aad2_cfg
        aad2_cfg["aad2_docker_home"] = aad2_home

    if sets:
        for item in sets:
            if "=" not in item:
                print(f"Error: Invalid --set '{item}'. Expected KEY=VALUE.", file=sys.stderr)
                sys.exit(1)
            k, v = item.split("=", 1)
            _apply_dotted_set(local_host, k.strip(), v.strip())

    fs_paths = copy.deepcopy(src_data.get("filesystem_paths") or {})
    sec_paths = copy.deepcopy(src_data.get("secure_inputs_paths") or {})

    active_entities = entities if entities is not None else (local_host.get("entities_available") or [])
    ctx = {"name": local_host.get("name", ""), "port": local_host.get("port") or ""}

    if fs_template is not None:
        fs_paths.update(_expand_entity_paths(fs_template, active_entities, ctx))
    if inputs_template is not None:
        sec_paths.update(_expand_entity_paths(inputs_template, active_entities, ctx))

    if entities is not None:
        _filter_by_entities(local_host, fs_paths, sec_paths, entities)

    if drop_remote_hosts:
        hosts = [local_host]

    cloned_dict: Dict[str, Any] = {
        "date": datetime.datetime.now().isoformat(),
        "hosts": hosts,
        "filesystem_paths": fs_paths,
        "secure_inputs_paths": sec_paths,
    }

    _write_ic_file(dest_path, cloned_dict, minify=minify)
    print(f"Cloned '{source_path}' -> '{dest_path}' (host='{local_host.get('name')}', port={local_host.get('port')}).")
    return dest_path
