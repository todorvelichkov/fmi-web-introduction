import socket

HOST = "127.0.0.1"
PORT = 9000


# By default, socket.socket creates TCP sockets.
with socket.socket() as server_sock:
    # This tells the kernel to reuse sockets that are in `TIME_WAIT` state.
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # This tells the socket what address to bind to.
    server_sock.bind((HOST, PORT))

    # 0 is the number of pending connections the socket may have before
    # new connections are refused.  Since this server is going to process
    # one connection at a time, we want to refuse any additional connections.
    server_sock.listen(0)
    print("Listening on {HOST}:{PORT}...".format(HOST=HOST, PORT=PORT))

    # it’ll print to standard out that it’s listening on 127.0.0.1:9000 and then exit.
    # In order to actually process incoming connections we need to call the accept method on our socket.
    # Doing so will block the process until a client connects to our server.
    client_sock, client_addr = server_sock.accept()
    print("New connection from {client_addr}.".format(client_addr=client_addr))

    # Once we have a socket connection to the client, we can start to communicate with it.
    # Using the sendall method, let’s send the connecting client an example response:
    with client_sock:
        response = '\r\n'.join([
            'HTTP/1.1 200 OK',
            'Content-type: text/html',
            'Content-length: 15',
            '',
            '<h1>Hello!</h1>',
        ])
        client_sock.sendall(response.encode())