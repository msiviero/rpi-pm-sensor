import selectors
import types
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
from threading import Timer

host = '127.0.0.1'
port = 50000


def serve(cb, interval):
    value = [('', '')]

    start_value = cb()
    if start_value is not None:
        value[0] = start_value

    def on_tick(current_value):
        try:
            new_value = cb()
            if new_value is not None:
                current_value[0] = new_value
        finally:
            Timer(interval, on_tick, args=(current_value,)).start()

    Timer(interval, on_tick, args=(value,)).start()

    selector = selectors.DefaultSelector()
    with socket(AF_INET, SOCK_STREAM) as server_socket:
        try:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen()
            print('listening', (host, port))
            server_socket.setblocking(False)
            selector.register(server_socket, selectors.EVENT_READ, data=None)

            while True:
                events = selector.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        current_socket = key.fileobj
                        connection, address = current_socket.accept()  # Should be ready to read
                        print('accepted connection', address)
                        connection.setblocking(False)
                        data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
                        events = selectors.EVENT_READ | selectors.EVENT_WRITE
                        selector.register(connection, events, data=data)
                    else:
                        sock = key.fileobj
                        data = key.data
                        if mask & selectors.EVENT_READ:
                            received_data = sock.recv(8)  # Should be ready to read
                            if received_data and received_data == b'RX':
                                data.outb += bytes(value[0], encoding="utf8")
                            else:
                                print('closing connection to', data.addr)
                                selector.unregister(sock)
                                sock.close()
                        if mask & selectors.EVENT_WRITE:
                            if data.outb:
                                print('sending', repr(data.outb), 'to', data.addr)
                                sent = sock.send(data.outb)
                                data.outb = data.outb[sent:]
        except KeyboardInterrupt:
            server_socket.close()


def read_socket_value():
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'RX')
        data = s.recv(16)

    return data


if __name__ == '__main__':
    print(read_socket_value())
