#!/usr/bin/env python3
import sys
import os
import argparse
import json

GEMSHOME = os.environ.get("GEMSHOME", "")
if GEMSHOME not in sys.path:
    sys.path.append(GEMSHOME)

from gemsModules.configuration.main_api import InstanceConfig, _load_instance_config
from gemsModules.configuration.control_script import (
    generate_from_tui,
    export_host,
    import_host,
    print_tui_help
)

def get_ic_path(custom_path=None):
    if custom_path:
        return custom_path
    from gemsModules.systemoperations.environment_ops import find_instance_config
    try:
        return find_instance_config()
    except Exception:
        return os.path.join(GEMSHOME, "instance_config.json")

def cmd_validate(args):
    path = get_ic_path(args.ic_file)
    if not os.path.exists(path):
        print(f"Validation Error: Configuration file '{path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    try:
        _load_instance_config(path)
        print("Validation Successful: IC is present and readable.")
    except Exception as e:
        print(f"Validation Failed: {e}", file=sys.stderr)
        sys.exit(1)

def cmd_evaluate(args):
    path = get_ic_path(args.ic_file)
    try:
        ic = _load_instance_config(path)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
        
    local_host = ic.get_localhost()
    print("=== Configuration Evaluation ===")
    if local_host:
        print(f"Local Host: {local_host.name} ({local_host.address})")
        print(f"  Served Entities: {[e.value for e in local_host.entities_available] if local_host.entities_available else []}")
    else:
        print("Local Host: NOT DEFINED")
        
    external_hosts = []
    if ic.hosts:
        for h in ic.hosts:
            if str(h.is_localhost).lower() != "true":
                external_hosts.append(h)
                
    print("\nExternal Hosts:")
    for h in external_hosts:
        print(f"  - {h.name} ({h.address})")
        print(f"    Served Entities: {[e.value for e in h.entities_available] if h.entities_available else []}")

def cmd_report_capabilities(args):
    path = get_ic_path(args.ic_file)
    try:
        ic = _load_instance_config(path)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
        
    target_host = None
    if ic.hosts:
        for h in ic.hosts:
            if h.name == args.host:
                target_host = h
                break
                
    if not target_host:
        print(f"Error: Host '{args.host}' not found in IC.", file=sys.stderr)
        sys.exit(1)
        
    print(json.dumps(target_host.dict(), indent=2))

def cmd_check_connectivity(args):
    path = get_ic_path(args.ic_file)
    try:
        ic = _load_instance_config(path)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
        
    result = ic.check_remote_host_connectivity(args.host)
    print(json.dumps(result, indent=2))

def cmd_confirm_capabilities(args):
    path = get_ic_path(args.ic_file)
    try:
        ic = _load_instance_config(path)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
        
    result = ic.confirm_remote_host_capabilities(args.host)
    print(json.dumps(result, indent=2))

def cmd_status(args):
    path = get_ic_path(args.ic_file)
    try:
        ic = _load_instance_config(path)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("=== Status Report ===")
    cmd_evaluate(args)
    
    external_hosts = []
    if ic.hosts:
        for h in ic.hosts:
            if str(h.is_localhost).lower() != "true":
                external_hosts.append(h)
                
    print("\n=== Remote Host Connectivity Checks ===")
    for h in external_hosts:
        print(f"Checking {h.name}...")
        res = ic.confirm_remote_host_capabilities(h.name)
        print(json.dumps(res, indent=2))

def main():
    # Handle the specific TUI/CLI args syntax from the Design Doc:
    # generate --from-file <filename>
    # generate --use-tui
    # export localhost [--to-file <filename>]
    # export host="name" [--to-file <filename>]
    # import --from-file <filename>
    
    # Custom parsing to match the exact syntax requested
    argv = sys.argv[1:]
    
    if not argv:
        print("Usage: instance_config <command> [args...]")
        print("Commands: generate, export, import, validate, evaluate, report, check-connectivity, confirm-capabilities, status")
        sys.exit(1)
        
    cmd = argv[0]
    
    # Check for help
    if len(argv) > 1 and argv[-1] == "help":
        if cmd == "generate":
            print_tui_help()
            sys.exit(0)
            
    if cmd == "generate":
        # Parse generate arguments
        parser = argparse.ArgumentParser(prog="instance_config generate")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--from-file", type=str, help="Path to input configuration JSON file.")
        group.add_argument("--use-tui", action="store_true", help="Start the interactive Q/A configuration tool.")
        parser.add_argument("--ic-file", type=str, help="Alternate output file name.")
        parser.add_argument("--minify", action="store_true", help="Write minified JSON (default is unminified).")
        args = parser.parse_args(argv[1:])
        
        if args.use_tui:
            generate_from_tui()
        elif args.from_file:
            # Read from file and save
            with open(args.from_file) as f:
                data = json.load(f)
            dest = args.ic_file if args.ic_file else "instance_config.json"
            indent = None if args.minify else 2
            with open(dest, "w") as f:
                json.dump(data, f, indent=indent)
            print(f"Configuration written to {dest}")
            
    elif cmd == "export":
        parser = argparse.ArgumentParser(prog="instance_config export")
        parser.add_argument("target", help="Either 'localhost' or 'host=name'")
        parser.add_argument("--to-file", type=str, help="File to write export to.")
        parser.add_argument("--ic-file", type=str, help="Alternate input configuration file.")
        args = parser.parse_args(argv[1:])
        
        ic_path = get_ic_path(args.ic_file)
        if args.target.startswith("host="):
            host_name = args.target.split("=", 1)[1].strip('"').strip("'")
        else:
            host_name = args.target
            
        export_host(ic_path, host_name, to_file=args.to_file)
        
    elif cmd == "import":
        parser = argparse.ArgumentParser(prog="instance_config import")
        parser.add_argument("--from-file", required=True, help="Export file from remote host.")
        parser.add_argument("--ic-file", type=str, help="Alternate output configuration file.")
        args = parser.parse_args(argv[1:])
        
        ic_path = get_ic_path(args.ic_file)
        import_host(ic_path, args.from_file, out_ic_path=args.ic_file)
        
    else:
        # Standard GEMS services parser
        parser = argparse.ArgumentParser(prog="instance_config")
        subparsers = parser.add_subparsers(dest="subcommand")
        
        subparsers.add_parser("validate").add_argument("--ic-file", type=str)
        subparsers.add_parser("evaluate").add_argument("--ic-file", type=str)
        
        p_report = subparsers.add_parser("report")
        p_report.add_argument("host")
        p_report.add_argument("--ic-file", type=str)
        
        p_conn = subparsers.add_parser("check-connectivity")
        p_conn.add_argument("host")
        p_conn.add_argument("--ic-file", type=str)
        
        p_conf = subparsers.add_parser("confirm-capabilities")
        p_conf.add_argument("host")
        p_conf.add_argument("--ic-file", type=str)
        
        subparsers.add_parser("status").add_argument("--ic-file", type=str)
        
        args = parser.parse_args(argv)
        
        if args.subcommand == "validate":
            cmd_validate(args)
        elif args.subcommand == "evaluate":
            cmd_evaluate(args)
        elif args.subcommand == "report":
            cmd_report_capabilities(args)
        elif args.subcommand == "check-connectivity":
            cmd_check_connectivity(args)
        elif args.subcommand == "confirm-capabilities":
            cmd_confirm_capabilities(args)
        elif args.subcommand == "status":
            cmd_status(args)

if __name__ == "__main__":
    main()
