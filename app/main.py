# Uncomment this to pass the first stage
import socket
import re


RESPONSE_HEADERS = {
    200: "HTTP/1.1 200 OK",
    404: "HTTP/1.1 404 Not Found",
}

CONTENT_TYPE = "Content-Type: text/plain"


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
            lines = request_data.split("\r\n")
            self._method, self._path, version = lines[0].split(" ")
        except (UnicodeDecodeError, IndexError, ValueError) as e:
            raise ValueError("Invalid HTTP request data") from e

    @property
    def method(self) -> str:
        return self._method

    @property
    def path(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f"HTTPRequestParser(method='{self._method}', path='{self._path}')"


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


def build_response(lines: list[str], body):
    """Builds a complete HTTP response.

    Args:
        lines: A list of strings representing the HTTP headers.
        body: The response body as a string.

    Returns:
        The complete HTTP response as a string.
    """
    response = "\r\n".join(lines)
    response += f"\r\n\r\n{body}\r\n\r\n"

    return response


def main():
    PORT = 4221  # ? Port number

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", PORT), reuse_port=True)

    print(f"Server started. Waiting for connections on port {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()  # wait for client

        request_data = HTTPRequestParser(
            client_socket.recv(1024)
        )  # Read data, up to 1024B

        path = request_data.path  # Request's path
        method = request_data.method  # Request's method

        response = ""

        match (method):
            case "GET":
                # If is just the path "/"
                if path == "/":
                    response = build_status_line(200, True)
                # If the path contains the "echo" word
                elif "echo" in path:
                    path_string = extract_string(
                        path
                    )  # The random string after "/echo/"
                    response = build_response(
                        [
                            build_status_line(200),  # Response status
                            CONTENT_TYPE,  # Content type header
                            f"Content-Length: {len(path_string)}",  # Body length
                        ],
                        path_string,  # Body
                    )
                # If the requested path is different from "/" returns 404
                else:
                    response = build_status_line(404, True)
            case _:
                print(f"Unsupported method: {request_data.method}")

        print("Connection info:")
        print(f"\tAddress: {client_address}")
        print(f"\tData: {request_data.__repr__}")
        print(f"\tResponse: \n{response}")
        print(f"\tEncoded: \n{response.encode()}")

        client_socket.sendall(response.encode())  # Send the response

        client_socket.close()  # Close the connection
        # server_socket.close() # Shutdown server


if __name__ == "__main__":
    main()
