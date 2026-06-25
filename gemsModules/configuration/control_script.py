#!/usr/bin/env python3
import sys
import os
import json
import datetime
from typing import Dict, List, Any

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
    hosts = config.get("hosts", [])
    target_host = None
    if host_name.lower() == "localhost":
        for h in hosts:
            if str(h.get("is_localhost", "False")).lower() == "true":
                target_host = h
                break
    else:
        for h in hosts:
            if h.get("name") == host_name:
                target_host = h
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
    else:
        print(out_str)
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
    local_hosts = {h["name"]: h for h in local_config.get("hosts", [])}
    remote_hosts = remote_config.get("hosts", [])
    
    for rh in remote_hosts:
        # Remote hosts should never be marked as localhost in local IC
        rh_copy = rh.copy()
        rh_copy["is_localhost"] = "False"
        name = rh_copy["name"]
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
