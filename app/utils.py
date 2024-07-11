import re
import os


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


def search_file(directory: str, f_name: str):
    """Checks if a file exists in a directory.

    Args:
        directoy (str): The directory of the file.
        name (str): The name of the file

    Returns:
        dict: A dictionary containing the content and size of the file.
    """
    output = {"exist": True, "content": "", "size": 0}
    f_path = f"{directory}{f_name}.txt"
    print(f_path)
    try:
        with open(f_path, "r") as f:
            f_content = f.read()
            f_size = os.path.getsize(f_path)

            output["content"] = f_content
            output["size"] = f_size

    except Exception as e:
        output["exist"] = False

    return output
