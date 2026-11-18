#!/usr/bin/env python3
import sys
import os
import argparse
import json

GEMSHOME = os.environ.get("GEMSHOME", "")
if not GEMSHOME:
    candidate = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if os.path.isdir(os.path.join(candidate, "gemsModules")):
        GEMSHOME = candidate
        os.environ["GEMSHOME"] = GEMSHOME

if GEMSHOME not in sys.path:
    sys.path.append(GEMSHOME)

from gemsModules.configuration.main_api import InstanceConfig, _load_instance_config
from gemsModules.configuration.control_script import (
    generate_from_tui,
    generate_from_matrix,
    clone_ic,
    ports_to_matrix,
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
        print("Commands: generate, clone, ports-to-matrix, export, import, validate, evaluate, report, check-connectivity, confirm-capabilities, status, init-gemsrc, show-config")
        sys.exit(1)
        
    cmd = argv[0]
    
    # Check for help
    if len(argv) > 1 and argv[-1] == "help":
        if cmd == "generate":
            print_tui_help()
            sys.exit(0)

    if cmd == "ports-to-matrix":
        parser = argparse.ArgumentParser(prog="instance_config ports-to-matrix")
        parser.add_argument("ports_file", help="Path to PORTS_dat.bash file.")
        parser.add_argument("--to", dest="to_path", default=None, help="Output matrix JSON file path (default: stdout).")
        parser.add_argument("--base", dest="base_path", default=None, help="Optional base JSON file to merge into the matrix 'base' section.")
        parser.add_argument("--cluster-name", dest="cluster_name", default=None, help="Override cluster name in matrix 'base'.")
        args = parser.parse_args(argv[1:])
        ports_to_matrix(
            ports_path=args.ports_file,
            to_path=args.to_path,
            base_path=args.base_path,
            cluster_name=args.cluster_name,
        )

    elif cmd == "generate":
        # Parse generate arguments
        parser = argparse.ArgumentParser(prog="instance_config generate")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--from-file", type=str, help="Path to input configuration JSON file.")
        group.add_argument("--use-tui", action="store_true", help="Start the interactive Q/A configuration tool.")
        group.add_argument("--matrix", type=str, help="Path to cluster matrix JSON file to generate multiple IC variants.")
        parser.add_argument("--ic-file", type=str, help="Alternate output file name (used with --from-file).")
        parser.add_argument("--output-dir", type=str, help="Output directory for files generated with --matrix.")
        parser.add_argument("--minify", action="store_true", help="Write minified JSON (default is unminified).")
        args = parser.parse_args(argv[1:])
        
        if args.use_tui:
            generate_from_tui()
        elif args.matrix:
            generate_from_matrix(args.matrix, output_dir=args.output_dir, minify=args.minify)
        elif args.from_file:
            # Read from file and save
            with open(args.from_file) as f:
                data = json.load(f)
            dest = args.ic_file if args.ic_file else "instance_config.json"
            indent = None if args.minify else 2
            with open(dest, "w") as f:
                json.dump(data, f, indent=indent)
            print(f"Configuration written to {dest}")

    elif cmd == "clone":
        parser = argparse.ArgumentParser(prog="instance_config clone")
        parser.add_argument("source", help="Path to source Instance Config JSON file.")
        parser.add_argument("--to", "--ic-file", dest="dest", required=True, help="Output path for the cloned IC file.")
        parser.add_argument("--name", type=str, default=None, help="Override localhost name.")
        parser.add_argument("--address", type=str, default=None, help="Override localhost address.")
        parser.add_argument("--port", type=str, default=None, help="Override localhost port (use 'none' to clear).")
        parser.add_argument("--entities", type=str, default=None, help="Comma- or space-separated list of entities_available (scopes partitions and paths).")
        parser.add_argument("--fs-template", type=str, default=None, help="Template for filesystem_paths (e.g. '/scratch/gems/ad/{entity}').")
        parser.add_argument("--inputs-template", type=str, default=None, help="Template for secure_inputs_paths (e.g. '/scratch/gems/ad/{entity}/inputs').")
        parser.add_argument("--website-envs", type=str, default=None, help="Comma- or space-separated website_environments.")
        parser.add_argument("--exec-envs", type=str, default=None, help="Comma- or space-separated execution_environments.")
        parser.add_argument("--aad2-home", type=str, default=None, help="Override resource_specific_information.aad2_configuration.aad2_docker_home.")
        parser.add_argument("--set", dest="sets", action="append", default=None, help="Override any localhost field using dotted path KEY=VALUE (repeatable).")
        parser.add_argument("--drop-remote-hosts", action="store_true", help="Drop non-localhost hosts from the cloned IC.")
        parser.add_argument("--minify", action="store_true", help="Write minified JSON.")
        args = parser.parse_args(argv[1:])

        def _split_list(val):
            if val is None:
                return None
            return [p for p in val.replace(",", " ").split() if p]

        clone_ic(
            source_path=args.source,
            dest_path=args.dest,
            name=args.name,
            address=args.address,
            port=args.port,
            entities=_split_list(args.entities),
            fs_template=args.fs_template,
            inputs_template=args.inputs_template,
            website_envs=_split_list(args.website_envs),
            exec_envs=_split_list(args.exec_envs),
            aad2_home=args.aad2_home,
            sets=args.sets,
            drop_remote_hosts=args.drop_remote_hosts,
            minify=args.minify,
        )
            
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
            
        out_json = export_host(ic_path, host_name, to_file=args.to_file)
        if not args.to_file:
            print(out_json)
        
    elif cmd == "import":
        parser = argparse.ArgumentParser(prog="instance_config import")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--from-file", type=str, help="Export file from remote host.")
        group.add_argument("--from-remote", type=str, help="Remote host gRPC target (e.g. 172.16.4.2:42059 or host_name).")
        parser.add_argument("--ic-file", type=str, help="Alternate output configuration file.")
        args = parser.parse_args(argv[1:])
        
        ic_path = get_ic_path(args.ic_file)
        if args.from_file:
            import_host(ic_path, args.from_file, out_ic_path=args.ic_file)
        elif args.from_remote:
            if ":" in args.from_remote:
                addr, port = args.from_remote.split(":", 1)
            else:
                ic = _load_instance_config(ic_path)
                target_h = None
                if ic.hosts:
                    for h in ic.hosts:
                        if h.name == args.from_remote:
                            target_h = h
                            break
                if not target_h or not target_h.port:
                    print(f"Error: Host '{args.from_remote}' not found or missing port in configuration.", file=sys.stderr)
                    sys.exit(1)
                addr, port = target_h.address, target_h.port
            ic = _load_instance_config(ic_path)
            res = ic.fetch_and_import_remote_host(addr, port, ic_path=ic_path)
            print(json.dumps(res, indent=2))
        
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
        
        p_init_rc = subparsers.add_parser("init-gemsrc")
        p_init_rc.add_argument("--output", "-o", type=str, default=None, help="Target path for .gemsrc (default: ~/.gemsrc)")

        subparsers.add_parser("show-config")
        
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
        elif args.subcommand == "init-gemsrc":
            from gemsModules.configuration.user_config import generate_sample_gemsrc
            dest = args.output or os.path.expanduser("~/.gemsrc")
            generate_sample_gemsrc(dest)
            print(f"Sample .gemsrc created at: {dest}")
        elif args.subcommand == "show-config":
            from gemsModules.configuration import user_config
            rc_file = user_config.find_gemsrc_path()
            print(f"Active .gemsrc: {rc_file or 'None (using system defaults)'}")
            print(f"GEMSHOME: {user_config.get_effective_gemshome()}")
            print(f"Instance Config: {user_config.get_effective_instance_config_path()}")
            print(f"Logs Directory: {user_config.get_effective_logs_dir()}")
            print(f"Output Directory: {user_config.get_effective_output_dir() or 'Default'}")
            print(f"Uploads Directory: {user_config.get_effective_uploads_dir() or 'Default'}")
            print(f"Log Level: {user_config.get_effective_logging_level() or 'error (default)'}")

if __name__ == "__main__":
    main()
