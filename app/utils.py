import re

def extract_string(path):
    return re.search(r"\/echo\/(.+)", path).group(1)