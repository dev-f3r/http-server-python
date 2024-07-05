from server import HTTPServer

if __name__ == "__main__":
    server = HTTPServer(host="localhost", port=4221)
    server.start()