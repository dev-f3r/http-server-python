import asyncio
from request_handler import RequestHandler

class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        # This method is now synchronous and runs the asyncio event loop
        asyncio.run(self._run_server())

    async def _run_server(self):
        # This is the asynchronous method that sets up and runs the server
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        print(f"Server running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        handler = RequestHandler(reader, writer)
        await handler.handle()