from re import findall, search, split
from db import database_controller
from commands import BC, AC, AD, AW, AB, AR, BA, BN



class service:
    def __init__(self):
        self.dbc = database_controller()



    def command_handler(self, command_string):
        if command_string == "BC":
            print()

        if command_string == "AC":
            ac = AC(self.dbc)
            ac.execute()

        if search("AD", command_string):
            command_data = split(" ", command_string)
            print(command_data[2])
            ad = AD(self.dbc)
            ad.execute(int(command_data[2]))




test = service()
test.command_handler("AC") #AD <account>/<ip> 20