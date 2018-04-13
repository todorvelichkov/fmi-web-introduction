import socket
import typing

HOST = "127.0.0.1"
PORT = 9000


def iter_lines(sock, bufsize=16384):
    """Given a socket, read all the individual CRLF-separated lines
    and yield each one until an empty one is found.  Returns the
    remainder after the empty line.
    """
    buff = b""
    while True:
        data = sock.recv(bufsize)
        if not data:
            return b""

        buff += data
        while True:
            try:
                i = buff.index(b"\r\n")
                line, buff = buff[:i], buff[i + 2:]
                if not line:
                    return buff

                yield line
            except IndexError:
                break


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

    while True:
        # process upcoming connection
        client_sock, client_addr = server_sock.accept()
        print("New connection from {client_addr}.".format(client_addr=client_addr))

        with client_sock:
            for request_line in iter_lines(client_sock):
                print(request_line)

            response = '\r\n'.join([
                'HTTP/1.1 200 OK',
                'Content-type: text/html',
                'Content-length: 15',
                '',
                '<h1>Hello %s!</h1>' % client_addr[1],
            ])
            client_sock.sendall(response.encode())
