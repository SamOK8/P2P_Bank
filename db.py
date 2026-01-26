import json


class database_controller:
    def __init__(self, lock):
        self.lock = lock

    def load_db(self):
        with open("db.json", "r") as db:
            return json.load(db)

    def save_db(self, data):
        with open("db.json", "w") as db:
            json.dump(data, db, indent=2)


    def add_account(self):
        with self.lock:
            data = self.load_db()
            print(data)
            account_number = data["lastAc"] + 1

            if account_number < 10000:
                account_number = 10000
            if account_number > 99999:
                raise ValueError("account limit reached")

            for acc in data["accounts"]:
                if acc["accountNumber"] == account_number:
                    raise ValueError("account already exists")

            data["accounts"].append({
                    "accountNumber": account_number,
                    "balance": 0
                })

            data["lastAc"] = account_number
            self.save_db(data)
            return account_number

    def del_account(self, account_number):
        with self.lock:
            data = self.load_db()
            data["accounts"].pop(self.get_account_index(data, account_number))
            self.save_db(data)

    def get_account_index(self, data, account_number):
        for i, acc in enumerate(data["accounts"]):
            if acc["accountNumber"] == account_number:
                return i
        raise ValueError("account does not exist")

    def get_balance(self, account_number):
        data = self.load_db()
        return int(data["accounts"][self.get_account_index(data, account_number)]["balance"])

    def acc_deposit(self, account_number, amount):
        with self.lock:
            data = self.load_db()

            idx = self.get_account_index(data, account_number)
            data["accounts"][idx]["balance"] += amount

            self.save_db(data)

    def acc_withdrawal(self, account_number, amount):
        with self.lock:
            data = self.load_db()

            idx = self.get_account_index(data, account_number)
            balance = data["accounts"][idx]["balance"]

            if balance < amount:
                raise ValueError("not enough funds")

            data["accounts"][idx]["balance"] -= amount

            self.save_db(data)

    def get_total_amount(self):
        data = self.load_db()
        total = 0
        for acc in data["accounts"]:
            total += acc["balance"]
        return total

    def get_number_of_accounts(self):
        data = self.load_db()
        return len(data["accounts"])



