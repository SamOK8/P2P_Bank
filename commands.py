
class BC:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self):
        return "BC" # + ip address


class AC:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self):
        account_number = self.dbc.add_account()
        return "AC" + str(account_number) + "/" # + ip address


class AD:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, account_number, amount):
        self.dbc.acc_deposit(account_number, amount)


class AW:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, account_number, amount):
        self.dbc.acc_withdrawal(account_number, amount)


class AB:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self):
        print()


class AR:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self):
        print()


class BA:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self):
        print()


class BN:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self):
        print()