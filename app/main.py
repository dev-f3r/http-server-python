from server import HTTPServer
import sys

if __name__ == "__main__":
    server = HTTPServer(host="localhost", port=4221, argv=sys.argv)
    server.start()