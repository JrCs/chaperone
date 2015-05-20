import asyncio
from functools import partial

class ServerProtocol(asyncio.Protocol):

    @classmethod
    def buildProtocol(cls, **kwargs):
        return partial(cls, **kwargs)

    def __init__(self, **kwargs):
        """
        Copy keywords directly into attributes when each protocol is created.
        This creates flexibility so that various servers can pass information to protocols.
        """
        
        for k,v in kwargs.items():
            setattr(self, k, v)
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

class Server:

    server = None

    def run(self):
        loop = asyncio.get_event_loop()
        listen = self._create_server()
        future = asyncio.async(listen)
        future.add_done_callback(self._run_done)
        return future

    def _run_done(self, f):
        # Handle errors here!
        self.server = f.result()
        print("IN SHARED _run_done", self.server)

    def close(self):
        s = self.server
        if s:
            if isinstance(s, tuple):
                s = s[0]
            print("CLOSING", self)
            s.close()