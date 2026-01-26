import socket
import random
import threading
from tcp_server import TCPServer
from web.web_server import WebServer

MIN_PORT = 65525
MAX_PORT = 65535
MAX_TRIES = 20

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def find_free_port():
    for _ in range(MAX_TRIES):
        port = random.randint(MIN_PORT, MAX_PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("0.0.0.0", port))
            sock.close()
            return port
        except OSError:
            continue
    raise Exception(f"Není volný port v rozsahu {MIN_PORT}-{MAX_PORT}")

def main():
    ip = get_local_ip()
    port = find_free_port()

    tcp_server = TCPServer(ip, port)

    # TCP server v threadu
    tcp_thread = threading.Thread(target=tcp_server.start, daemon=True)
    tcp_thread.start()

    # Web server
    web = WebServer(tcp_server, web_port=8080)
    web.start()

if __name__ == "__main__":
    main()
