import json


class database_controller:

    def load_db(self):
        with open("db.json", "r") as db:
            return json.load(db)

    def save_db(self, data):
        with open("db.json", "w") as db:
            json.dump(data, db, indent=2)


    def add_account(self, account_number, balance):
        data = self.load_db()
        print(data)
        for acc in data["accounts"]:
            if acc["accountNumber"] == account_number:
                raise ValueError("account already exists")

        data["accounts"].append({
                "accountNumber": account_number,
                "balance": balance
            })

        self.save_db(data)



    def get_account_index(self, data, account_number):
        for i, acc in enumerate(data["accounts"]):
            if acc["accountNumber"] == account_number:
                return i
        raise ValueError("account does not exist")

    def acc_deposit(self, account_number, amount):
        data = self.load_db()

        idx = self.get_account_index(data, account_number)
        data["accounts"][idx]["balance"] += amount

        self.save_db(data)

    def acc_withdrawal(self, account_number, amount):
        data = self.load_db()

        idx = self.get_account_index(data, account_number)
        balance = data["accounts"][idx]["balance"]

        if balance < amount:
            raise ValueError("not enough funds")

        data["accounts"][idx]["balance"] -= amount

        self.save_db(data)

