import re
from re import findall, search, split
from db import database_controller
from commands import BC, AC, AD, AW, AB, AR, BA, BN



class service:
    def __init__(self, lock, ip_address):
        self.dbc = database_controller(lock)
        self.server_ip = ip_address



    def command_handler(self, command_string):
        ACCOUNT = r"(?P<account>[1-9]\d{4})"
        IP = r"(?P<ip>(?:\d{1,3}\.){3}\d{1,3})"
        AMOUNT = r"(?P<amount>\d+)"
        AD_AW_REGEX = re.compile(
            rf"^(?P<cmd>AD|AW) {ACCOUNT}/{IP} {AMOUNT}$"
        )
        AB_AR_REGEX = re.compile(
            rf"^(?P<cmd>AB|AR) {ACCOUNT}/{IP}$"
        )

        if command_string == "BC":
            return BC(self.dbc).execute()

        if command_string == "AC":
            return AC(self.dbc).execute()

        AD_AW = AD_AW_REGEX.match(command_string)
        if AD_AW:
            cmd = AD_AW.group("cmd")
            account = int(AD_AW.group("account"))
            amount = int(AD_AW.group("amount"))

            if cmd == "AD":
                return AD(self.dbc).execute(account, amount)
            else:
                return AW(self.dbc).execute(account, amount)

        AB_AR = AB_AR_REGEX.match(command_string)
        if AB_AR:
            cmd = AB_AR.group("cmd")
            account = int(AB_AR.group("account"))

            if cmd == "AB":
                return AB(self.dbc).execute(account)
            else:
                return AR(self.dbc).execute(account)

        raise ValueError("Invalid command")




#test = service()
# print(test.command_handler("AC"))
# print(test.command_handler("AD 10001/192.168.1.22 20"))
# print(test.command_handler("AB 10001/192.168.1.22"))
# print(test.command_handler("AR 10004/192.168.1.22"))