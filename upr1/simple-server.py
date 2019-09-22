import socket
from urllib.parse import quote, unquote

HOST = "127.0.0.1"
PORT = 9000

#resources: https://defn.io/2018/02/25/web-app-from-scratch-01/

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
        # it’ll print to standard out that it’s listening on 127.0.0.1:9000 and then exit.
        # In order to actually process incoming connections we need to call the accept method on our socket.
        # Doing so will block the process until a client connects to our server.
        client_sock, client_addr = server_sock.accept()
        print("New connection from {client_addr}.".format(client_addr=client_addr))

        # Once we have a socket connection to the client, we can start to communicate with it.
        # Using the sendall method, let’s send the connecting client an example response:
        with client_sock:
            lines = [request_line for request_line in iter_lines(client_sock)]
            # Decode: From Bytes to Unicode
            request_path = unquote(lines[0].decode().split(' ')[1])
            response_body = '<html><body>Hello <strong>%s</strong> You are at: %s</body></html>' % (client_addr[1], request_path)
            response = '\r\n'.join([
                'HTTP/1.1 200 OK',
                'Content-Type: text/html; charset=utf-8',
                'Content-length: %s' % len(response_body),
                '',
                response_body
            ]).encode() # From Unicode to Bytes
            client_sock.sendall(response)