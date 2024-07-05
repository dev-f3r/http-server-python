from constants import RESPONSE_HEADERS, CONTENT_TYPE


class ResponseBuilder:
    @staticmethod
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

    @staticmethod
    def build_response(lines, body, close_connection=True):
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
