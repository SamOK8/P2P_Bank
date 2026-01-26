import socket
import threading
from tcp_handler import TCPHandler
from command_handler import CommandHandler
from bank import Bank

class TCPServer:
    def __init__(self, host="0.0.0.0", port=65525):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = False

        self.bank = Bank()
        self.command_handler = CommandHandler(self.host, self.port, self.bank)

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
        except OSError:
            print(f"[!] Port {self.port} je obsazený")
            return

        self.server_socket.listen()
        self.is_running = True

        print(f"[+] TCP Server běží na {self.host}:{self.port}")

        while self.is_running:
            client_socket, address = self.server_socket.accept()
            handler = TCPHandler(
                client_socket,
                address,
                self.command_handler
            )

            threading.Thread(target=handler.handle, daemon=True).start()

    def stop(self):
        self.is_running = False
        self.server_socket.close()

    def send_command(self, ip, port, command, timeout=5):
        try:
            with socket.create_connection((ip, port), timeout=timeout) as sock:
                sock.sendall((command + "\n").encode("utf-8"))
                return sock.recv(4096).decode("utf-8").strip()
        except Exception as e:
            return f"ER {e}"