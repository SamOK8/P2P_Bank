from ipaddress import ip_address


class BC:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, ip_address):
        return "BC " + ip_address


class AC:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, ip_address):
        account_number = self.dbc.add_account()
        return "AC " + str(account_number) + "/" + ip_address


class AD:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, account_number, amount):
        self.dbc.acc_deposit(account_number, amount)
        return "AD"


class AW:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, account_number, amount):
        self.dbc.acc_withdrawal(account_number, amount)
        return "AW"


class AB:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, account_number):
        return "AB " + str(self.dbc.get_balance(account_number))


class AR:
    def __init__(self, dbc):
        self.dbc = dbc

    def execute(self, account_number):
        self.dbc.del_account(account_number)
        return "AR"


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