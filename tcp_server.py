import multiprocessing
import socket
import random
from tcp_handler import TCPHandler
from service import service


class TCPServer:
    def __init__(self, host="0.0.0.0"):
        self.host = host
        self.port = self._bind_random_port()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = multiprocessing.Lock()
        self.service = service(ip_address=self.host, lock=self.lock)
        self.is_running = False
        self.peers = {}

    def _bind_random_port(self):
        for _ in range(20):
            port = random.randint(65525, 65535)
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.bind(("0.0.0.0", port))
                test_socket.close()
                return port
            except OSError:
                continue
        raise RuntimeError("Nelze najít volný port")

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.is_running = True

        print(f"[+] Bank node běží na {self.host}:{self.port}")

        while self.is_running:
            client_socket, address = self.server_socket.accept()
            handler = TCPHandler(client_socket, address, self)
            p = multiprocessing.Process(
                target=handler.handle,
                daemon=True
            )
            p.start()

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

    def handle_command(self, command: str) -> str:
        command = command.strip()

        if "/" not in command:
            return self.service.command_handler(command)

        try:
            account_part = command.split()[1]
            target_ip = account_part.split("/")[1]
        except IndexError:
            return "ER invalid command format"

        if target_ip == self.host:
            return self.service.command_handler(command)

        return self.forward_to_peer(target_ip, command)

    def forward_to_peer(self,target_ip, command: str) -> str:
        try:

            if target_ip not in self.peers:
                port = self.discover_peer_port(target_ip)
                if port is None:
                    return "ER Peer bank not reachable"

                self.peers[target_ip] = port

            return self.send_command(target_ip, self.peers[target_ip], command)
        except Exception as e:
            return f"ER forwarding failed: {e}"

    def discover_peer_port(self, ip, timeout=0.3):
        """
        Prohledá porty 65525–65535 a najde bank node
        """
        for port in range(65525, 65536):
            try:
                with socket.create_connection((ip, port), timeout=timeout) as sock:
                    sock.sendall(b"BC\n")
                    resp = sock.recv(1024).decode("utf-8").strip()

                    if resp.startswith("BC"):
                        print(f"[DISCOVER] Bank nalezena {ip}:{port}")
                        return port

            except (socket.timeout, ConnectionRefusedError, OSError):
                continue

        return None

