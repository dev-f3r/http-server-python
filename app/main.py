# Uncomment this to pass the first stage
import socket
from dataclasses import dataclass

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

        request_data = HTTPRequestParser(client_socket.recv(1024))  # Read data, up to 1024B

        response = "HTTP/1.1 200 OK\r\n\r\n"  # HTTP 200 response

        match (request_data.method):
            case "GET":
                # If the requested path is different from "/" returns 404
                if request_data.path != "/":
                    response = "HTTP/1.1 404 Not Found\r\n\r\n"
            case _:
                print(f"Unsupported method: {request_data.method}")

        print("Conection info:")
        print(f"\tAddress: {client_address}")
        print(f"\tData: {request_data.__repr__}")
        print(f"\tResponse: {response}")

        client_socket.sendall(response.encode())  # Send the response

        client_socket.close()  # Close the connection
        # server_socket.close() # Shutdown server


if __name__ == "__main__":
    main()
