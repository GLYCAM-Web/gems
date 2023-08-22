import logging
import grpc
import concurrent.futures as futures

from abc import abstractmethod, ABC


log = logging.getLogger(__name__)


class SimpleGRPCServer(ABC):
    Servicer = None
    PB_GRPC_MODULE = None

    def __init__(self, port=51151):
        self.port = port

        self.pool = futures.ThreadPoolExecutor(max_workers=10)

        self.server = grpc.server(self.pool)
        self.server.add_insecure_port(f"[::]:{port}")

        if self.Servicer is None or self.PB_GRPC_MODULE is None:
            raise NotImplementedError("Servicer and GRPC_STUB must be defined")
        else:
            servicer_name = self.Servicer.__bases__[-1].__name__
            add_to_server = getattr(
                self.PB_GRPC_MODULE, f"add_{servicer_name}_to_server"
            )
            add_to_server(self.Servicer(), self.server)

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop(0)
        self.pool.shutdown(wait=True)

    def join(self):
        self.server.wait_for_termination()


class SimpleGRPCClient(ABC):
    STUB_TYPE = None
    PB_MODULE = None

    def __init__(self, host):
        self.host = host

        self._stub = None
        self._pb_module = None
        self._channel = None

    @property
    def protobuf(self):
        return self.PB_MODULE

    @property
    def stub(self):
        if self._stub is None:
            self._stub = self.STUB_TYPE(self.channel)
        return self._stub

    @property
    def channel(self):
        if self._channel is None:
            self._channel = grpc.insecure_channel(self.host)
        return self._channel

    def close(self):
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    def send_request(self, request):
        log.debug(f"Querying {self.host} with {request}...")
        response = self.get_response(request)
        log.debug(f"Response: {response}")
        return response

    @abstractmethod
    def get_response(self, request):
        pass
