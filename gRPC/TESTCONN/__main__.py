#!/usr/bin/env python3
import argparse
import json
import multiprocessing
import os
import importlib
import sys
import logging
from importlib import util
from pathlib import Path
import time
import traceback

log = logging.getLogger(__name__)

# This script needs a few thigns to run correctly on bare metal: grpcio, grpcio-tools, pydantic==1.8.1, and gmml.


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
    """Dynamic import of a module relative to GEMSHOME."""
    gemsroot = Path(GEMSHOME())
    rootpath = gemsroot
    rel_path = Path(rel_path)

    # parent=1 means we will be looking at siblings of GEMSHOME in the Web_Programs directory, such as GRPC.
    # Because this case is so common, we will enforce GRPC's parent to be 1.
    if rel_path.parts[0] == "GRPC":
        parent = 1

        if util.find_spec("grpc") is None or util.find_spec("grpc_tools") is None:
            raise RuntimeError(
                "Please ensure Python's GRPC package is installed when using GRPC scripts.\n\tLikely fix: `pip install grpcio==1.46.3 grpcio-tools==1.46.3`"
            )

    # TODO\Q: If we make gmml an installable package/library, we can do something like this to check for gmml:
    # if util.find_spec("gmml") is None:
    #
    # Instead, we'll just see if gmml.py exists in GEMSHOME for now:
    if not (gemsroot / "gmml.py").exists():
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


def argparser():
    """

    Program arguments
        --server "port"
            - Run the script as a GRPC server on "port"
            - Use this to start a GRPC listener on machine A with GEMS installed.
        --client ["host:port"]:
            -  Run the script as a GRPC client attempting to connect to "host:port"
            -  Use this to attempt to connect to a GRPC listener on machine B with GEMS installed.
                - If the connection is successful, the GRPC client will send a message to the GRPC server.
                    - If there is a network gap, Machine A's port will need to be to the internet for this to work.
                    ~ If Machine A is actually a docker container, the container will need to be connected to the internet and the port may need to be exposed.
                - If the connection is unsuccessful, the GRPC client will print an error message.
    """
    parser = argparse.ArgumentParser(
        description="Run this script as a GRPC client or server."
    )

    parser.add_argument(
        "--server",
        dest="server",
        action="store_true",
        help='Run the script as a GRPC server on on "port"',
    )
    parser.add_argument(
        "--client",
        dest="client",
        action="store_true",
        help='Run the script as a GRPC client attempting to connect to "host:port"',
    )

    parser.add_argument(
        "--host",
        dest="host",
        default="localhost:51151",
    )

    args = parser.parse_args()
    args.port = int(args.host.split(":")[1])
    return args


from server import main as _server_main
from client import MinClient as Client


def server_main(port):
    log.debug(f"Server thread started, attempting to listen on port {port}...")
    try:
        _server_main(port=port)
    except Exception as e:
        log.debug(traceback.format_exc())
        log.error(f"Server thread failed to start: {e}")
    except KeyboardInterrupt:
        log.info(f"Stopping server thread...")


def client_main(host):
    log.debug(f"Client thread started, attempting to connect to {host}...")

    response = Client(host).send_request(r"Hello world!")

    # Returning just the output to avoid certain pickling complications.
    log.debug(f"Client thread finished, stopping...")
    return response.message


def main():
    """This python script is useful for ensuring a GRPC connection can be established between two GEMS installs."""
    logging.basicConfig(
        level=logging.DEBUG, format="%(levelname)s:%(module)s:%(message)s"
    )
    args = argparser()

    with multiprocessing.Pool() as pool:
        if args.server:
            pool.apply_async(server_main, args=(args.port,))

        if args.client:
            if args.server:
                # Can be crucial if the server is slow to start or client is started too quickly after the server.
                time.sleep(1)

            asy_res = pool.apply_async(client_main, args=(args.host,))
            log.debug("Trying to get the response from the client...")
            try:
                response = asy_res.get()
            except multiprocessing.pool.MaybeEncodingError as e:
                log.debug("The client thread errored.")
                log.debug(traceback.format_exc())

                print(
                    "\n--- FAILURE ---\nClient thread had an issue pickling some data."
                )
                exit(1)

            log.debug(f"Client got this response: {response}")
            if response is not None:
                print(
                    "\n--- SUCCESS ---\nClient got an expected response, connection over GRPC is working."
                )
                exit(0)
            else:
                print("\n--- FAILURE ---\nClient didn't receive a valid response.")
                exit(1)

        # Wait for all threads to finish (Keep main thread alive for server thread, primarily.)
        pool.close()
        pool.join()


if __name__ == "__main__":
    main()
