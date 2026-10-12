# User Configuration and Standalone GEMS Guide

## 1. Overview & Motivation

Historically, GEMS was designed primarily for execution in a single-owner or web-server container environment. This led to assumptions that caused friction and fatal crashes when GEMS was used standalone or executed by a user other than the owner of the `GEMSHOME` source tree:

1. **Hardcoded Log Directory**: Log handlers wrote directly to `$GEMSHOME/logs/`. If a non-owner user ran GEMS (or if GEMS was installed in a read-only or shared directory like `/shared/gems`), initializing logging raised an unhandled `PermissionError: [Errno 13] Permission denied`.
2. **Mandatory Environment Variables**: Scripts and modules failed immediately if `GEMSHOME` was not explicitly exported in the user's shell.
3. **Hardcoded Instance Configuration**: GEMS searched only for `$GEMSHOME/instance_config.json`, preventing individual users on a shared installation from specifying their own execution topologies or remote host configurations.
4. **Restricted Output Paths**: Non-website runs defaulted outputs to container paths (e.g., `/work/`) or `$GEMSHOME/UserSpace`, which failed on standard workstations or multi-user clusters.

To resolve these limitations, GEMS includes a **Standalone & User Configuration System** driven by `user_config.py` and optional `.gemsrc` configuration files.

---

## 2. Configuration Discovery Hierarchy

When resolving configuration options, GEMS evaluates settings in the following order of precedence:

1. **Environment Variables**:
   - `GEMS_RC` or `GEMSRC`: Path to a custom `.gemsrc` file.
   - `GEMSHOME`: Explicit GEMS installation root.
   - `GEMS_INSTANCE_CONFIG`: Path to instance configuration JSON.
   - `GEMS_LOG_DIR` / `GEMS_LOGS_DIR`: Path to application logs directory.
   - `GEMS_LOGING_LEVEL`: Verbosity level (`error`, `info`, `debug`).
   - `GEMS_OUTPUT_DIR`: Default directory for project outputs.
   - `GEMS_UPLOADS_DIR`: Default directory for uploaded input files.
   - `GEMS_VENV`: Path to a custom virtual environment.

2. **`.gemsrc` Configuration File**:
   If not specified by `GEMS_RC`, GEMS automatically searches for `.gemsrc` in:
   - Current working directory: `./.gemsrc` or `./gemsrc`
   - User home directory: `~/.gemsrc`
   - XDG configuration paths: `~/.config/gems/gemsrc` or `~/.config/gems/config.json`
   - User `.gems` folder: `~/.gems/gemsrc` or `~/.gems/config.json`
   - GEMS home directory: `$GEMSHOME/.gemsrc`

3. **Intelligent System Defaults & Auto-Detection**:
   - If `GEMSHOME` is unset, GEMS automatically determines its root from the location of the codebase.
   - If `$GEMSHOME/logs/` is not writable, GEMS automatically falls back to `~/.gems/logs/`, `/tmp/gems-<user>/logs/`, or standard error stream logging.
   - If no custom output directory is specified, GEMS falls back to `~/GEMS_UserSpace`.

---

## 3. Configuration Formats & Keys

The `.gemsrc` file supports both **INI / key-value format** and **JSON format**. Values automatically expand tildes (`~`) and shell environment variables (`$VAR`).

### Supported Keys

| Key | Description | Default Fallback |
| :--- | :--- | :--- |
| `gemshome` / `gems_home` | Root directory of GEMS | Auto-detected from codebase path |
| `instance_config` / `instance_config_path` | Path to `instance_config.json` | `./instance_config.json` or `$GEMSHOME/instance_config.json` |
| `log_dir` / `logs_dir` | Directory where logs are written | `$GEMSHOME/logs` (if writable), else `~/.gems/logs` or `/tmp` |
| `logging_level` / `log_level` | Logging verbosity (`error`, `info`, `debug`) | `error` |
| `output_dir` / `userspace_dir` | Destination for project run outputs | `~/GEMS_UserSpace` |
| `uploads_dir` | Destination for user uploaded inputs | `~/GEMS_UserSpace/uploads` |
| `venv_path` / `venv_dir` | Python virtual environment path | `$GEMSHOME/.venv` (if present) |

---

## 4. Example Configurations

### INI / Key-Value Format (`~/.gemsrc`)

```ini
[gems]
# Override logs to a writable personal folder
log_dir = ~/.gems/logs
logging_level = info

# Direct outputs to scratch or project storage
output_dir = /scratch/my_user/gems_runs
uploads_dir = /scratch/my_user/gems_runs/uploads

# Custom instance configuration for cluster routing
instance_config = ~/my_cluster_instance_config.json
```

### JSON Format (`~/.gemsrc` or `~/.config/gems/config.json`)

```json
{
  "log_dir": "~/.gems/logs",
  "logging_level": "info",
  "output_dir": "~/my_research/docking_outputs",
  "uploads_dir": "~/my_research/docking_outputs/uploads",
  "instance_config": "~/instance_config.json"
}
```

---

## 5. Sample Standalone Instance Configuration (`instance_config.json.example`)

For users and developers running GEMS standalone or testing via the CLI, a template is provided at:
`$GEMSHOME/instance_config.json.example`

### Key Highlights:
- **Local Standalone Execution**: Configures `local-standalone` (`localhost`) to support all GEMS entities (`AD`, `BC`, `CB`, `GM`, `GP`, `MD`, `PDB`).
- **Developer CLI Remote Tunnel (`thortunnel`)**: Pre-configures a remote host entry for `localhost:42099`. When developing or testing remote build/slurm services over an SSH tunnel (e.g., `ssh -L 42099:localhost:42099 webdev@thoreau`), scripts like `test_build_remote.sh` and `./bin/delegate` work immediately without manual JSON editing.
- **Host Resource-Specific Information (`resource_specific_information`)**: Contains host-specific resources and tool configurations needed for request fulfillment (e.g., batch scheduler settings like Slurm and tool configurations like `aad2_configuration`).
- **User-Relative Storage Paths**: Points filesystem output directories to `GEMS_UserSpace/` rather than hardcoded `/website/userdata/`.

### Host Resource-Specific Information & `aad2_configuration`

The `resource_specific_information` block on each host in the Instance Configuration holds information required for request fulfillment on that specific machine. For Antibody Docking (AAD2), this eliminates hardcoded host paths:

```json
{
  "resource_specific_information": {
    "use_gres_for_gpus": "True",
    "cpu_hardware_equivalent": "core",
    "aad2_configuration": {
      "aad2_docker_home": "/path/to/AAD2_Docker",
      "aad2_cli_bin_path": "/path/to/AAD2_Docker/image/AAD2/bin",
      "image": "antibody-docking:tag",
      "vmd_home": "/path/to/vmd/bin",
      "vmd_lib": "/path/to/vmd/lib"
    }
  }
}
```

#### Fields & Resolution Rules:
- `aad2_docker_home`: Root path to `AAD2_Docker`. Can also be overridden by the environment variable `AAD2_DOCKER_HOME`.
- `aad2_cli_bin_path`: Directory containing CLI tools (`submit_docking_to_slurm_with_docker.bash`). Automatically defaults to `{aad2_docker_home}/image/AAD2/bin`.
- `image`: Docker/Singularity image tag. If omitted, GEMS attempts to discover the image tag from `{aad2_docker_home}/settings.bash`.
- `ad2cliconfig_example_file`: Template file for CLI configs. Automatically defaults to `{aad2_docker_home}/image/AAD2/99.cluster_utilities/ad2cliconfig.example`.
- **Notice Handling**: If `aad2_docker_home` is neither configured in the IC nor exported as `AAD2_DOCKER_HOME`, GEMS returns a JSON response containing an Error Notice (`Brief="PathNotConfigured"`, `Code="404"`) rather than crashing or falling back to hardcoded `/programs` or `/home` paths.

### Quick Setup:
```bash
# Copy template to user's home directory or current working directory:
cp $GEMSHOME/instance_config.json.example ~/.gems/instance_config.json

# Validate with GEMS CLI:
./bin/instance_config.py validate --ic-file ~/.gems/instance_config.json
```

---

## 6. Built-in CLI Utilities

Users can inspect active configurations or initialize a `.gemsrc` using GEMS command-line tools:

### Inspect Active Configuration
```bash
./bin/instance_config.py show-config
```
Output:
```
Active .gemsrc: /home/alice/.gemsrc
GEMSHOME: /shared/programs/gems
Instance Config: /home/alice/my_cluster_instance_config.json
Logs Directory: /home/alice/.gems/logs
Output Directory: /scratch/alice/gems_runs
Uploads Directory: Default
Log Level: info
```

### Generate Sample `.gemsrc`
```bash
# Creates ~/.gemsrc with pre-filled paths
./bin/instance_config.py init-gemsrc

# Or generate at a custom path
./bin/instance_config.py init-gemsrc --output ./workspace.gemsrc
```

You can also run the module directly:
```bash
python3 -m gemsModules.configuration.user_config --init
```

---

## 6. Resilience & Non-Owner Safety Guarantees

1. **Zero Permission Crashes**: If log file creation fails due to filesystem permissions, GEMS logs to `sys.stderr` and continues execution without crashing.
2. **Zero Missing Environment Crashes**: Scripts like `bin/delegate` automatically detect the GEMS repository root if `$GEMSHOME` is unset in the user's shell.
3. **Multi-User Isolation**: Multiple users sharing a single GEMS repository can write to separate project output directories and log files without file collision or permission errors.
