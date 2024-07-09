from http_parser import HTTPRequestParser
from response_builder import ResponseBuilder
from utils import extract_string, connection_info
from constants import CONTENT_TYPE


class RequestHandler:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.parser = None
        self.response_builder = ResponseBuilder()

    async def handle(self):
        """
        Handles the request and sends the response to the client.
        """
        data = await self.reader.read(1024)
        self.parser = HTTPRequestParser(data)
        response = self.process_request(self.parser.method)
        await self.send_response(response)

    def process_request(self, method):
        """
        Processes the request and returns the response.

        Args:
            method: The HTTP method of the request.

        Returns:
            The response to send to the client.
        """

        response = b""

        match (method):
            case "GET":
                # If path just "/", responds with 200 OK.
                if self.parser.path == "/":
                    response = self.response_builder.build_status_line(
                        200, True
                    )  # Builds a simple reponse.

                # If path "/echo/<something else>", sends the length of <something else> as body.
                elif "echo" in self.parser.path:
                    status_line = self.response_builder.build_status_line(
                        200
                    )  # Build status line.
                    path_string = extract_string(
                        self.parser.path
                    )  # Extract the string after "echo".

                    response = self.response_builder.build_response(
                        [
                            status_line,
                            CONTENT_TYPE,
                        ],
                        path_string,
                    )  # Builds full response.

                # If path "/user-agent", sends the length of user-agent as body.
                elif "user-agent" in self.parser.path:
                    status_line = self.response_builder.build_status_line(
                        200
                    )  # Build status line.

                    response = self.response_builder.build_response(
                        [
                            status_line,
                            CONTENT_TYPE,
                        ],
                        self.parser.user_agent,
                    )  # Builds full response.

                # Otherwise returns 404.
                else:
                    response = self.response_builder.build_status_line(404, True)

            case _:
                print(f"Unsupported method: {self.parser.method}")

        return response

    async def send_response(self, response):
        """
        Sends the response to the client and closes the connection.

        Args:
            response: The response to send.
        """

        # Prints the info about the request
        connection_info(
            response=response, address=self.writer.get_extra_info("peername")
        )

        # Writes the response to the client
        self.writer.write(response.encode())

        # Drains the writer
        await self.writer.drain()

        # Closes the connection
        self.writer.close()
