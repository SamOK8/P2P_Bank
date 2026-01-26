from flask import Flask, render_template
import socket

LOG_FILE = "logs/bank.log"

class WebServer:
    def __init__(self, tcp_server, web_port=8080):
        self.tcp_server = tcp_server
        self.web_port = web_port
        self.app = Flask(__name__, template_folder="templates")

        self.app.add_url_rule("/", "index", self.index)

    def index(self):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = f.read()
        except FileNotFoundError:
            logs = "Log soubor nenalezen."

        return render_template(
            "index.html",
            bank_ip=self.tcp_server.host,
            bank_port=self.tcp_server.port,
            logs=logs
        )

    def start(self):
        self.app.run(
            host="0.0.0.0",
            port=self.web_port,
            debug=False,
            use_reloader=False
        )
