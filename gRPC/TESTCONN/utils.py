import os
import logging
import sys

from importlib import util
from pathlib import Path

log = logging.getLogger(__name__)


# TODO: find the appropriate place to put this function. It's a helper useful in many places, particularly outside gemsModules.
def GEMSHOME():
    GEMSHOME = os.getenv("GEMSHOME")
    if GEMSHOME is None:
        raise RuntimeError(
            "GEMSHOME is not set. Please ensure GEMS is installed correctly and set GEMSHOME to the GEMS installation."
        )
    return GEMSHOME


# TODO: see above
def safe_gems_relative_import(rel_path, parent=0, exec_=True):
    """Dynamic import of a module relative to GEMSHOME.


    GEMS is not a real package, so we can't use the normal importlib machinery.

    """
    gemsroot = Path(GEMSHOME())
    rootpath = gemsroot
    rel_path = Path(rel_path)

    # parent=1 means we will be looking at siblings of GEMSHOME in the Web_Programs directory, such as GRPC.
    # Because this case is so common, we will enforce GRPC's parent to be 1.
    if rel_path.parts[0] == "GRPC":
        parent = 1

        if util.find_spec("grpc") is None or util.find_spec("grpc_tools") is None:
            raise RuntimeError(
                "Please ensure Python's GRPC package is installed when using GRPC scripts.\n\tLikely fix: `pip install grpcio grpcio-tools` (>=1.59.2)"
            )

    # TODO\Q: If we make gmml an installable package/library, we can do something like this to check for gmml:
    # if util.find_spec("gmml") is None:
    #
    # Instead, we'll just see if gmml.py (and _gmml.so) exists in GEMSHOME for now:
    if not (gemsroot / "gmml.py").exists() or not (gemsroot / "_gmml.so").exists():
        log.warning(
            "Please ensure Python's gmml package is installed. Usually gmml is installed into gems, see the DevEnv docs for more details."
        )

    # Check pydantic
    if util.find_spec("pydantic") is None:
        log.warning("If you encounter GEMS API bugs, please install Pydantic.")

    while parent > 0:
        rootpath = rootpath.parent
        parent -= 1

    sys.path.append(str(rootpath / rel_path.parent))

    spec = util.spec_from_file_location(rel_path.stem, rootpath / rel_path)
    mod = util.module_from_spec(spec)

    if exec_:
        spec.loader.exec_module(mod)

    return mod


def host_from_env(args):
    # example hosts:
    # $GRPC_DELEGATOR_HOST:$GRPC_DELEGATOR_PORT
    # $GEMS_GRPC_SLURM_HOST:$GEMS_GRPC_SLURM_PORT
    try:
        slurm_host = (
            f"{os.getenv('GEMS_GRPC_SLURM_HOST')}:{os.getenv('GEMS_GRPC_SLURM_PORT')}"
        )
    except TypeError:
        log.warning("This container is not configured to use GEMS_GRPC_SLURM_HOST.")
        slurm_host = None

    try:
        delegator_host = (
            f"{os.getenv('GRPC_DELEGATOR_HOST')}:{os.getenv('GRPC_DELEGATOR_PORT')}"
        )
    except TypeError:
        log.warning("This container is not configured to use GRPC_DELEGATOR_HOST.")
        delegator_host = None

    # If we don't use a special keyword, it will just pass through the "host:port"
    if args.host == "delegator":
        args.host = delegator_host
    elif args.host == "slurm":
        args.host = slurm_host
    elif args.host == "conntest":
        args.host = f"{os.getenv('GRPC_DELEGATOR_HOST')}:51151"

    if args.host is None:
        raise ValueError("No valid host provided.")

    return args
