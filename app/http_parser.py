
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
