# Uncomment this to pass the first stage
import socket
# import mycoloredtext as mct

def main():
    PORT = 4221 # ? Port number

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", PORT), reuse_port=True)

    print(f"Server started. Waiting for connections on port {PORT}")

    while True:
        client_socket, client_address = server_socket.accept()  # wait for client

        request_data = client_socket.recv(1024)  # Read data, up to 1024B

        print("Conection info:")
        print(f"\tAddress: {client_address}")
        print(f"\tData: {request_data}")
        # mct.print_gnb("Conection info:")
        # mct.print_bb(f"\tAddress: {client_address}")
        # mct.print_yb(f"\tData: {request_data}")

        response = "HTTP/1.1 200 OK\r\n\r\n"  # HTTP 200 response

        client_socket.sendall(response.encode())  # Send the response

        client_socket.close() # Close the connection
        # server_socket.close() # Shutdown server


if __name__ == "__main__":
    main()
