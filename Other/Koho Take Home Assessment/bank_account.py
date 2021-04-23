import datetime
from datetime import timedelta


class BankAccount:

    daily_max = 5000.00
    weekly_max = 20000.00
    daily_loads = 3


    def __init__(self, customer_id):
        self_customer_id = customer_id
        self.ids = set()
        self.transactions = {}


    def load_account(self, transaction_json):
        # Extracting metadata
        transaction_id =  transaction_json["id"]

        if transaction_id in self.ids:
            pass
        else:
            self.ids.add(transaction_id)
            customer_id = transaction_json["customer_id"]
            load_amount = float(transaction_json["load_amount"].strip("$"))
            date = datetime.datetime.strptime(transaction_json["time"], "%Y-%m-%dT%H:%M:%SZ").date()
            week_trunc = date - datetime.timedelta(days= date.weekday())
            week_key = "Week " + str(week_trunc)

            # Creating response object
            response = {}
            response["id"] = transaction_id
            response["customer_id"] = customer_id

            # Performing checks
            check_daily_limit = False
            check_weekly_limit = False
            check_daily_loads = False

            if week_key not in self.transactions:
                check_daily_loads = True
                if load_amount <= BankAccount.daily_max:
                    check_daily_limit = True
                    check_weekly_limit = True          
            if week_key in self.transactions:
                week_value = 0
                for key, value in self.transactions[week_key].items():
                    week_value += sum(value["load_amounts"])
                if load_amount + week_value <= BankAccount.weekly_max:
                    check_weekly_limit = True
                if str(date) not in self.transactions[week_key]:
                    check_daily_loads = True
                    if load_amount <= BankAccount.daily_max:
                        check_daily_limit = True
                if str(date) in self.transactions[week_key]:
                    if load_amount + sum(self.transactions[week_key][str(date)]["load_amounts"]) <= BankAccount.daily_max:
                        check_daily_limit = True
                    if len(self.transactions[week_key][str(date)]["ids"]) + 1 <= BankAccount.daily_loads:
                        check_daily_loads = True

            # Create log of transaction and response
            if check_weekly_limit and check_daily_limit and check_daily_loads:
                if week_key not in self.transactions:
                    self.transactions[week_key] = {}
                if str(date) not in self.transactions[week_key]:
                    self.transactions[week_key][str(date)]= {}
                    self.transactions[week_key][str(date)]["ids"] = []
                    self.transactions[week_key][str(date)]["load_amounts"] = []
                self.transactions[week_key][str(date)]["ids"].append(transaction_id)
                self.transactions[week_key][str(date)]["load_amounts"].append(load_amount)
                response["accepted"] = True
            else:
                response["accepted"] = False
        
            return response