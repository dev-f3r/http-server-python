# Uncomment this to pass the first stage
import socket
import re
import asyncio
from asyncio import StreamReader, StreamWriter

RESPONSE_HEADERS = {
    200: "HTTP/1.1 200 OK",
    404: "HTTP/1.1 404 Not Found",
}
CONTENT_TYPE = "Content-Type: text/plain"
PORT = 4221  # ? Port number


class HTTPRequestParser:
    """
    A class to parse and extract information from an HTTP request.

    Attributes:
        _method (str): The HTTP request method (e.g., GET, POST).
        _path (str): The requested path (e.g., /, /index.html).
    """

    def __init__(self, data: bytes) -> None:
        """
        Initializes the HTTPRequestParser object by parsing the HTTP request data.

        Args:
            data (bytes): The raw HTTP request data received from the client.

        Raises:
            ValueError: If the request data is malformed or cannot be decoded.
        """
        try:
            request_data = data.decode()
            self._lines = request_data.split("\r\n")

            self._method, self._path, self._http_version = self._lines[0].split(" ")

            # If the are more header that the first
            if self._lines[1] != "":
                self._host = self._lines[1].split(" ")[1]
                self._user_agent = self._get_agent(self._lines[1:])
            else:
                self._host = ""
                self._user_agent = ""

        except (UnicodeDecodeError, IndexError, ValueError) as e:
            raise ValueError("Invalid HTTP request data") from e

    def _get_agent(self, lines) -> str:
        """
        Extracts the user agent string from the HTTP request headers.

        Args:
            lines (list[str]): A list of strings representing the HTTP request headers.

        Returns:
            str: The user agent string, or an empty string if not found.
        """
        for line in lines:
            if "User-Agent" in line:
                return " ".join(line.split(" ")[1:])
        return ""

    @property
    def lines(self) -> list[str]:
        return self._lines

    @property
    def method(self) -> str:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    @property
    def user_agent(self) -> str:
        return self._user_agent


def build_status_line(code, end=False):
    """Builds the status line of an HTTP response.

    Args:
        code: The HTTP status code (e.g., 200, 404).
        end: A boolean indicating whether to add a double CRLF (\r\n\r\n) at the end to signal the end of headers.

    Returns:
        The HTTP status line.
    """
    line = RESPONSE_HEADERS[code]

    return line + "\r\n\r\n" if end else line


def extract_string(path):
    """Extracts the string within the angle brackets from a URL of the form /echo/<a-random-string>.

    Args:
        path: The URL path.

    Returns:
        The extracted string.
    """
    return re.search(r"\/echo\/(.+)", path).group(1)


def build_response(lines: list[str], body, close_connection=True):
    """Builds a complete HTTP response.

    Args:
        lines: A list of strings representing the HTTP headers.
        body: The response body as a string.

    Returns:
        The complete HTTP response as a string.
    """
    print(lines)
    response = "\r\n".join(lines) + "\r\n"
    response += f"Content-Length: {len(body)}"  # Content-Length header
    # if close_connection:
    #     response += "Connection: close\r\n"  # Close the connection if its needed.
    response += f"\r\n\r\n{body}\r\n\r\n"

    return response


async def handler(reader: StreamReader, writer: StreamWriter):
    data = await reader.read(1024)
    request_data = HTTPRequestParser(data)  # Read data, up to 1024B

    client_address = writer.get_extra_info("peername")  # Get the client address

    path = request_data.path  # Request's path
    method = request_data.method  # Request's method

    response = ""  # The response for the current request

    # ? Build the reponse based on the following cases
    match (method):
        case "GET":
            # If is just the path "/"
            if path == "/":
                response = build_status_line(200, True)
            # If the path contains the "echo" word
            elif "echo" in path:
                path_string = extract_string(path)  # The random string after "/echo/"
                response = build_response(
                    [
                        build_status_line(200),  # Response status
                        CONTENT_TYPE,  # Content type header
                    ],
                    path_string,  # Body
                )
            # If the path contains the "user-agent" word
            elif "user-agent" in path:
                user_agent = request_data._user_agent
                response = build_response(
                    [
                        build_status_line(200),
                        CONTENT_TYPE,
                    ],
                    user_agent,  # The request's user-agent as the body
                )
            # If the requested path is different from "/" returns 404
            else:
                response = build_status_line(404, True)
        case _:
            print(f"Unsupported method: {request_data.method}")

    # ? Prints the info about the requets
    print("Connection info:")
    print(f"\tAddress: {client_address}")
    print(f"\tData:")
    for line in request_data.lines:
        print(f"\t-{line}")  # Print each line of the request.
    print(f"\tResponse: \n{response}")

    # ? Send the response
    writer.write(response.encode()) # Buffered the response
    await writer.drain() # Send the response
    writer.close() # Close connection


async def main():
    server = await asyncio.start_server(handler, "localhost", PORT)  # Create the server

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    print(f"Listening connections on port {PORT}")

    async with server:
        await server.serve_forever() # Make listen multiple petitions


if __name__ == "__main__":
    asyncio.run(main()) # Run main coroutine with asyncio
