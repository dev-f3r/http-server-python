from http_parser import HTTPRequestParser
from response_builder import ResponseBuilder
from utils import extract_string
from constants import CONTENT_TYPE


class RequestHandler:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.parser = None
        self.response_builder = ResponseBuilder()

    async def handle(self):
        data = await self.reader.read(1024)
        self.parser = HTTPRequestParser(data)
        response = self.process_request(self.parser.method)
        await self.send_response(response)

    def process_request(self, method):
        response = b""

        match (method):
            case "GET":
                # If path just "/", responds with 200 OK.
                if self.parser.path == "/":
                    response = self.response_builder.build_status_line(
                        200, True
                    )  # Builds a simple reponse.

                # If path "/echo/<something else>", sends the length of<something else> as body.
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
                    ) # Builds full response.

                # If path "/user-agent", sends the length of user-agent as body.
                elif "user-agent" in self.parser.path:
                    status_line = self.response_builder.build_status_line(200) # Build status line.

                    response = self.response_builder.build_response(
                        [
                            status_line,
                            CONTENT_TYPE,
                        ],
                        self.parser.user_agent,
                    ) # Builds full response.

                # Otherwise returns 404.
                else:
                    response = self.response_builder.build_status_line(404, True)

            case _:
                print(f"Unsupported method: {self.parser.method}")

        return response

    async def send_response(self, response):
        # TODO: Print information about the request before send a response.
        # ? Prints the info about the requets
        print("Connection info:")
        print(f"\tAddress: {self.writer.get_extra_info('peername')}")
        # print(f"\tData:")
        # for line in request_data.lines:
        #     print(f"\t-{line}")  # Print each line of the request.
        print(f"\tResponse: \n{response}")

        
        self.writer.write(response.encode())
        await self.writer.drain()
        self.writer.close()
