# TESTCONN

A python script to test gRPC connection availability between two machines.

## Installation

If you're not running with a full GEMS installation, TESTCONN requires grpcio and grpcio-tools:
```bash
$ pip3 install grpcio==1.46.3 grpcio-tools==1.46.3
```

## Usage
Trivial in-process test of gRPC connection:
```bash
$ cd $GEMSHOME/gRPC
$ python TESTCONN -h [-v]
$ python TESTCONN --server --client # --host localhost:51151
```

Connection test between two containers:
```bash
V2$ bash bin/connect grpc delegator
user@gw-grpc-delegator$ cd $GEMSHOME/gRPC
user@gw-grpc-delegator:/programs/gems/gRPC$ python TESTCONN --server # --host localhost:51151

V2$ bash bin/connect slurm head
user@gw-slurm-head$ cd $GEMSHOME/gRPC
user@gw-slurm-head:/programs/gems/gRPC$ python TESTCONN --client --host gw-grpc-delegator:51151
```

### Example output
```bash
gems/gRPC$ python TESTCONN --server --client
DEBUG:__main__:server_main      | Server thread started, attempting to listen on port 51151...
INFO:__main__:server_main       | TESTCONN server started on port 51151.
DEBUG:__main__:main_entry       | Trying to get the response from the client...
DEBUG:__main__:client_main      | Client thread started, attempting to connect to localhost:51151...
DEBUG:minimal:send_request      | Querying localhost:51151 with Hello world!...
DEBUG:minimal:GetServerResponse | Servicer's gRPC Servicer has been called.
DEBUG:minimal:send_request      | Response: message: "hello world!\n"

DEBUG:__main__:client_main      | Client thread finished, stopping...
DEBUG:__main__:client_main      | Was this Response expected? yes
DEBUG:__main__:main_entry       | Client got this response: hello world!


--- CONNECTION SUCCESS ---
Client got a Response, connection over GRPC is working.
```

