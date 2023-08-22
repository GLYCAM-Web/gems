#!/usr/bin/env python3
import argparse
import multiprocessing
import logging
import time
import traceback

log = logging.getLogger(__name__)

# This script needs a few thigns to run correctly on bare metal: grpcio, grpcio-tools, pydantic==1.8.1, and gmml.


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
    # args = host_from_env(args)

    args.port = int(args.host.split(":")[1])
    return args


# Client / Server Threads
from modules.minimal import MinClient, MinServer


def client_main(host):
    log.debug(f"Client thread started, attempting to connect to {host}...")

    content = "Hello world!"

    response = MinClient(host).send_request(content)

    log.debug(f"Client thread finished, stopping...")
    log.debug(
        f"Was this Response expected? {'yes' if response.message[:-1] == content else 'no'}"
    )

    # Returning just the message to avoid certain pickling complications.
    return response.message


def server_main(port):
    log.debug(f"Server thread started, attempting to listen on port {port}...")
    try:
        server = MinServer(port)

        server.start()
        log.info("TESTCONN server started on port %s.", port)

        server.join()
    except Exception as e:
        log.debug(traceback.format_exc())
        log.error(f"Server thread failed to start: {e}")
    except KeyboardInterrupt:
        log.info(f"Stopping server thread...")

    finally:
        server.stop()


# Main Thread
def entry_main():
    """This python script is useful for ensuring a GRPC connection can be established between two GEMS installs."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(module)s:%(funcName)s\t| %(message)s",
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
            except multiprocessing.pool.MaybeEncodingError:
                log.debug("The client thread errored.")
                log.debug(traceback.format_exc())

                print(
                    "\n--- CONNECTION FAILURE ---\nClient thread had an issue pickling some data."
                )
                exit(1)

            log.debug(f"Client got this response: {response}")
            if response is not None:
                print(
                    "\n--- CONNECTION SUCCESS ---\nClient got a Response, connection over GRPC is working."
                )
                exit(0)
            else:
                print(
                    "\n--- CONNECTION FAILURE ---\nClient didn't receive a response. (got None)"
                )
                exit(1)

        # Wait for all threads to finish (Keep main thread alive for server thread, primarily.)
        pool.close()
        pool.join()


if __name__ == "__main__":
    entry_main()
