class TCPHandler:
    def __init__(self, client_socket, address, server):
        self.client_socket = client_socket
        self.address = address
        self.server = server

    def handle(self):
        print(f"[+] Připojen {self.address}")

        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                command = data.decode("utf-8").strip()
                print(f"[{self.address}] CMD = {repr(command)}")

                if not command:
                    continue

                try:
                    response = self.server.handle_command(command)
                except Exception as e:
                    response = f"ER {type(e).__name__}: {e}"

                self.client_socket.sendall((response + "\n").encode("utf-8"))

        except Exception as e:
            print(f"[!] Chyba {self.address}: {e}")

        finally:
            self.client_socket.close()
            print(f"[-] Odpojen {self.address}")
