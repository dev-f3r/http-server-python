import re

def extract_string(path):
    """
    Extracts the string after the word "echo" from a given path.

    Args:
        path: The path to extract the string from.

    Returns:
        The extracted string.
    """
    return re.search(r"\/echo\/(.+)", path).group(1)


def connection_info(response, address):
    """
    Prints the connection information.

    Args:
        response: The response object.
        address: The address of the client.
    """
    print("Connection info:")
    print(f"\tAddress: {address}")
    print(f"\tResponse: \n{response}")
