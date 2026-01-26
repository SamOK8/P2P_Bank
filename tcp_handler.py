from logger import log
from concurrent.futures import ThreadPoolExecutor, TimeoutError

executor = ThreadPoolExecutor(max_workers=10)

class TCPHandler:
    def __init__(self, client_socket, address, server):
        self.client_socket = client_socket
        self.address = address
        self.client_ip = address[0]
        self.client_port = address[1]
        self.server = server

    def handle(self):
        print(f"[+] Připojen {self.address}")
        log(f"CONNECT | {self.client_ip}:{self.client_port}")

        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                command = data.decode("utf-8").strip()
                print(f"[{self.address}] CMD = {repr(command)}")

                if not command:
                    continue

                log(f"IN  | {self.client_ip}:{self.client_port} | {command}")

                try:
                    future = executor.submit(
                        self.server.handle_command,
                        command
                    )
                    response = future.result(timeout=5)

                except TimeoutError:
                    response = "ER Timeout"
                    log(f"ERROR | {self.client_ip}:{self.client_port} | {response}")

                except Exception as e:
                    response = f"ER {e}"
                    log(f"ERROR | {self.client_ip}:{self.client_port} | {response}")



                log(f"OUT | {self.client_ip}:{self.client_port} | {response}")
                self.client_socket.sendall((response + "\r\n").encode("utf-8"))

        except Exception as e:
            log(f"ERROR | {self.client_ip}:{self.client_port} | {e}")
            print(f"[!] Chyba {self.address}: {e}")

        finally:
            self.client_socket.close()
            log(f"DISCONNECT | {self.client_ip}:{self.client_port}")
            print(f"[-] Odpojen {self.address}")
