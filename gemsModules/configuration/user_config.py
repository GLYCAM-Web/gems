#!/usr/bin/env python3
"""User and Standalone Configuration System for GEMS.

Provides automatic discovery and parsing of user-level and workspace-level
`.gemsrc` configuration files, as well as smart defaults for:
- GEMSHOME root detection
- Instance configuration discovery
- User log directories with automatic fallback on permission errors
- Output / UserSpace directories
- Uploads directories
- Virtual environment detection
"""

import os
import sys
import json
import configparser
from pathlib import Path
from typing import Any, Dict, Optional, Union

# Global cache for loaded .gemsrc settings
_CACHED_CONFIG: Optional[Dict[str, Any]] = None
_CACHED_CONFIG_FILE: Optional[str] = None


def get_current_user_name() -> str:
    """Safely determine current username across environments without throwing exceptions."""
    try:
        import getpass
        return getpass.getuser()
    except Exception:
        return os.environ.get("USER") or os.environ.get("LOGNAME") or str(os.getuid())


def is_directory_writable(path: Union[str, Path], make_if_needed: bool = True) -> bool:
    """Check if a directory exists and is writable, or can be created and written to."""
    if not path:
        return False
    target = Path(path).resolve()
    try:
        if not target.exists():
            if make_if_needed:
                target.mkdir(parents=True, exist_ok=True)
            else:
                return False

        if not target.is_dir():
            return False

        # Probe with a temporary test file write to guarantee true write permission
        test_file = target / f".gems_write_probe_{os.getpid()}"
        try:
            with open(test_file, "w") as f:
                f.write("probe\n")
            if test_file.exists():
                test_file.unlink()
            return True
        except (PermissionError, OSError):
            return False
    except (PermissionError, OSError):
        return False


def find_gemsrc_path() -> Optional[Path]:
    """Search for a .gemsrc file across standard configuration locations.

    Search precedence:
    1. GEMS_RC or GEMSRC environment variable
    2. Current working directory: ./.gemsrc or ./gemsrc
    3. User home directory: ~/.gemsrc
    4. XDG / user config directories:
       - $XDG_CONFIG_HOME/gems/gemsrc or ~/.config/gems/gemsrc
       - $XDG_CONFIG_HOME/gems/config.json or ~/.config/gems/config.json
       - ~/.gems/gemsrc or ~/.gems/config.json
    5. GEMSHOME directory: $GEMSHOME/.gemsrc (if GEMSHOME is known)
    """
    # 1. Environment variable override
    env_path = os.environ.get("GEMS_RC") or os.environ.get("GEMSRC")
    if env_path:
        p = Path(env_path).expanduser().resolve()
        if p.is_file():
            return p

    # 2. Current working directory
    for name in [".gemsrc", "gemsrc"]:
        cwd_p = Path.cwd() / name
        if cwd_p.is_file():
            return cwd_p

    # 3. User home directory
    home_dir = Path.home()
    user_p = home_dir / ".gemsrc"
    if user_p.is_file():
        return user_p

    # 4. XDG / user config directories
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    xdg_base = Path(xdg_config).expanduser() if xdg_config else home_dir / ".config"

    candidates = [
        xdg_base / "gems" / "gemsrc",
        xdg_base / "gems" / "config.json",
        home_dir / ".gems" / "gemsrc",
        home_dir / ".gems" / "config.json",
    ]
    for c in candidates:
        if c.is_file():
            return c

    # 5. GEMSHOME/.gemsrc
    gemshome = os.environ.get("GEMSHOME")
    if gemshome:
        gh_p = Path(gemshome).expanduser() / ".gemsrc"
        if gh_p.is_file():
            return gh_p

    return None


def parse_gemsrc(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Parse a .gemsrc file supporting both JSON and INI/key=value formats."""
    p = Path(file_path).expanduser().resolve()
    if not p.is_file():
        return {}

    content = p.read_text(encoding="utf-8").strip()
    if not content:
        return {}

    config_dict: Dict[str, Any] = {}

    # Try JSON parsing first
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            for k, v in data.items():
                norm_key = str(k).lower().strip().replace("-", "_")
                # Expand path strings containing ~ or $ENV
                if isinstance(v, str):
                    v = os.path.expanduser(os.path.expandvars(v))
                config_dict[norm_key] = v
            return config_dict
    except json.JSONDecodeError:
        pass

    # Try INI / key=value parsing
    try:
        cp = configparser.ConfigParser()
        # If no section header is found, pretend it is under [gems]
        if not content.startswith("["):
            cp.read_string(f"[gems]\n{content}")
        else:
            cp.read_string(content)

        # Select primary section: 'gems', 'default', or the first section
        section_name = "gems" if cp.has_section("gems") else (
            "default" if cp.has_section("default") else cp.sections()[0]
        )
        for k, v in cp.items(section_name):
            norm_key = k.lower().strip().replace("-", "_")
            if isinstance(v, str):
                v = os.path.expanduser(os.path.expandvars(v))
            config_dict[norm_key] = v
        return config_dict
    except Exception:
        pass

    return config_dict


def load_gemsrc(path: Optional[Union[str, Path]] = None, force_reload: bool = False) -> Dict[str, Any]:
    """Load configuration from .gemsrc, returning a dictionary of normalized settings."""
    global _CACHED_CONFIG, _CACHED_CONFIG_FILE

    if not force_reload and _CACHED_CONFIG is not None:
        return _CACHED_CONFIG

    target_path = Path(path) if path else find_gemsrc_path()
    if target_path and target_path.is_file():
        _CACHED_CONFIG = parse_gemsrc(target_path)
        _CACHED_CONFIG_FILE = str(target_path)
    else:
        _CACHED_CONFIG = {}
        _CACHED_CONFIG_FILE = None

    return _CACHED_CONFIG


def get_gemsrc_value(key: str, default: Any = None) -> Any:
    """Retrieve a single key from the loaded .gemsrc configuration."""
    cfg = load_gemsrc()
    norm_key = key.lower().strip().replace("-", "_")
    return cfg.get(norm_key, default)


def get_effective_gemshome() -> str:
    """Determine the effective GEMSHOME directory.

    Order of resolution:
    1. GEMSHOME environment variable (if non-empty)
    2. .gemsrc 'gemshome' or 'gems_home'
    3. Auto-detection relative to this module's filesystem path
    """
    env_val = os.environ.get("GEMSHOME")
    if env_val and env_val.strip():
        resolved = str(Path(env_val).expanduser().resolve())
        return resolved

    rc_val = get_gemsrc_value("gemshome") or get_gemsrc_value("gems_home")
    if rc_val:
        resolved = str(Path(rc_val).expanduser().resolve())
        os.environ["GEMSHOME"] = resolved
        return resolved

    # Auto-detect from module location (gemsModules/configuration/user_config.py -> ../../../)
    detected = Path(__file__).resolve().parent.parent.parent
    if (detected / "gemsModules").is_dir():
        resolved = str(detected)
        os.environ["GEMSHOME"] = resolved
        return resolved

    return str(detected)


def get_effective_logs_dir() -> str:
    """Determine a valid, writable logs directory for GEMS.

    Resolution order:
    1. GEMS_LOG_DIR or GEMS_LOGS_DIR environment variable
    2. .gemsrc 'logs_dir' or 'log_dir'
    3. GEMSHOME/logs (if writable)
    4. User home directory: ~/.gems/logs (if writable)
    5. Temporary directory: /tmp/gems-<user>/logs (if writable)
    6. System temp fallback: /tmp/gems-logs
    """
    env_dir = os.environ.get("GEMS_LOG_DIR") or os.environ.get("GEMS_LOGS_DIR")
    if env_dir:
        cand = Path(env_dir).expanduser().resolve()
        if is_directory_writable(cand):
            return str(cand)

    rc_dir = get_gemsrc_value("logs_dir") or get_gemsrc_value("log_dir")
    if rc_dir:
        cand = Path(rc_dir).expanduser().resolve()
        if is_directory_writable(cand):
            return str(cand)

    # Check GEMSHOME/logs
    try:
        gh_dir = Path(get_effective_gemshome()) / "logs"
        if is_directory_writable(gh_dir):
            return str(gh_dir)
    except Exception:
        pass

    # Check user home directory
    user_home_dir = Path.home() / ".gems" / "logs"
    if is_directory_writable(user_home_dir):
        return str(user_home_dir)

    # Check /tmp user directory
    user_name = get_current_user_name()
    tmp_user_dir = Path(f"/tmp/gems-{user_name}/logs")
    if is_directory_writable(tmp_user_dir):
        return str(tmp_user_dir)

    # Fallback to system /tmp
    tmp_fallback = Path("/tmp/gems-logs")
    if is_directory_writable(tmp_fallback):
        return str(tmp_fallback)

    return "/tmp"


def get_effective_instance_config_path() -> str:
    """Determine the instance configuration path.

    Order of resolution:
    1. GEMS_INSTANCE_CONFIG environment variable
    2. .gemsrc 'instance_config' or 'instance_config_path'
    3. ./instance_config.json (current working directory)
    4. ~/.gems/instance_config.json or ~/.config/gems/instance_config.json
    5. GEMSHOME/instance_config.json
    """
    env_path = os.environ.get("GEMS_INSTANCE_CONFIG")
    if env_path and env_path.strip():
        return str(Path(env_path).expanduser().resolve())

    rc_path = get_gemsrc_value("instance_config") or get_gemsrc_value("instance_config_path")
    if rc_path:
        cand = Path(rc_path).expanduser().resolve()
        if cand.is_file():
            return str(cand)

    # Check CWD
    cwd_ic = Path.cwd() / "instance_config.json"
    if cwd_ic.is_file():
        return str(cwd_ic.resolve())

    # Check ~/.gems or ~/.config/gems
    for cand_p in [
        Path.home() / ".gems" / "instance_config.json",
        Path.home() / ".config" / "gems" / "instance_config.json",
    ]:
        if cand_p.is_file():
            return str(cand_p.resolve())

    # Default to GEMSHOME/instance_config.json
    return str(Path(get_effective_gemshome()) / "instance_config.json")


def get_effective_output_dir() -> Optional[str]:
    """Retrieve user-configured filesystem output directory if specified."""
    env_dir = os.environ.get("GEMS_OUTPUT_DIR")
    if env_dir and env_dir.strip():
        return str(Path(env_dir).expanduser().resolve())

    rc_dir = (
        get_gemsrc_value("output_dir")
        or get_gemsrc_value("userspace_dir")
        or get_gemsrc_value("project_dir")
    )
    if rc_dir:
        return str(Path(rc_dir).expanduser().resolve())

    return None


def get_effective_uploads_dir() -> Optional[str]:
    """Retrieve user-configured filesystem uploads directory if specified."""
    env_dir = os.environ.get("GEMS_UPLOADS_DIR")
    if env_dir and env_dir.strip():
        return str(Path(env_dir).expanduser().resolve())

    rc_dir = get_gemsrc_value("uploads_dir")
    if rc_dir:
        return str(Path(rc_dir).expanduser().resolve())

    return None


def get_effective_logging_level() -> Optional[str]:
    """Retrieve user-configured logging level ('error', 'info', 'debug') if specified."""
    env_level = os.environ.get("GEMS_LOGGING_LEVEL")
    if env_level and env_level.strip():
        return env_level.strip().lower()

    rc_level = get_gemsrc_value("logging_level") or get_gemsrc_value("log_level")
    if rc_level:
        return str(rc_level).strip().lower()

    return None


def get_effective_venv_path() -> Optional[str]:
    """Retrieve user-configured virtual environment path if specified."""
    env_venv = os.environ.get("GEMS_VENV")
    if env_venv and env_venv.strip():
        return str(Path(env_venv).expanduser().resolve())

    rc_venv = get_gemsrc_value("venv_path") or get_gemsrc_value("venv_dir")
    if rc_venv:
        return str(Path(rc_venv).expanduser().resolve())

    return None


def generate_sample_gemsrc(dest_path: Optional[Union[str, Path]] = None) -> str:
    """Generate a sample .gemsrc configuration file."""
    home_dir = str(Path.home())
    gemshome = get_effective_gemshome()

    sample = f"""# GEMS User Configuration (.gemsrc)
# This file allows users other than the owner of GEMSHOME to configure
# local logging, custom project output directories, and instance configurations.
#
# Supported formats: JSON or key = value INI format.

[gems]
# GEMS installation directory (auto-detected if omitted)
gemshome = {gemshome}

# Path to instance configuration file
instance_config = {gemshome}/instance_config.json

# Directory for application log files (defaults to ~/.gems/logs or /tmp if GEMSHOME/logs is not writable)
log_dir = {home_dir}/.gems/logs

# Default logging level: error, info, or debug
logging_level = info

# Custom directory for project outputs (replaces default /work or GEMSHOME/UserSpace)
output_dir = {home_dir}/GEMS_UserSpace

# Custom directory for uploaded inputs/resources
uploads_dir = {home_dir}/GEMS_UserSpace/uploads

# Optional custom python virtual environment
# venv_path = {home_dir}/.venv-gems
"""
    if dest_path:
        p = Path(dest_path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(sample, encoding="utf-8")

    return sample


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--init", "-i", "init"):
        target = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / ".gemsrc"
        generate_sample_gemsrc(target)
        print(f"Created sample .gemsrc at: {target}")
    else:
        active_rc = _CACHED_CONFIG_FILE or find_gemsrc_path()
        print(f"Active .gemsrc: {active_rc or 'None (using system defaults)'}")
        print(f"Effective GEMSHOME: {get_effective_gemshome()}")
        print(f"Effective Logs Dir: {get_effective_logs_dir()}")
        print(f"Effective Instance Config: {get_effective_instance_config_path()}")
        print(f"Effective Output Dir: {get_effective_output_dir() or 'Default (GEMS_UserSpace/work)'}")
        print(f"Effective Uploads Dir: {get_effective_uploads_dir() or 'Default'}")
        print(f"Effective Log Level: {get_effective_logging_level() or 'error (default)'}")
