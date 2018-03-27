import grpc
import sys

from functools import partial


class ServiceClient:

    def __init__(self, service, stub_name, host, port, timeout=10):
        channel = grpc.insecure_channel('{0}:{1}'.format(host,port))
        try:
            grpc.channel_ready_future(channel).result(timeout=10)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to Todo Service...')

        self.stub = getattr(service, stub_name)(channel)
        self.timeout = timeout

    def __getattr__(self, attr):
        return partial(self._wrapped_call, self.stub, attr)

    @staticmethod
    def _wrapped_call(*args, **kwargs):
        try:
            return getattr(args[0], args[1])(
                args[2], **kwargs
            )
        except grpc.RpcError as e:
            print('Call {0} failed with {1}'.format(
                args[1], e.code()
            ))

            raise
