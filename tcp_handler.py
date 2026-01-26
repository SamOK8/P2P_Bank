
class TCPHandler:
    def __init__(self, client_socket, address, command_handler):
        self.client_socket = client_socket
        self.address = address
        self.command_handler = command_handler

    def handle(self):
        print(f"[+] Připojen klient {self.address}")

        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                message = data.decode("utf-8").strip()
                print(f"[{self.address}] {message}")

                response = self.command_handler.handle(message)
                self.client_socket.sendall((response + "\n").encode("utf-8"))

        except Exception as e:
            print(f"[!] Chyba {self.address}: {e}")

        finally:
            self.client_socket.close()
            print(f"[-] Odpojen klient {self.address}")
