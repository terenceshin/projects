import json
import bank_account as ba


customer_accounts = {}


def load_transactions(file_name):
    with open(file_name) as f:
        transactions = f.readlines()
        transactions = [json.loads(transaction.strip()) for transaction in transactions]
    return transactions


def process_transactions(transactions, output_file):
    for transaction in transactions:
        
        if transaction['customer_id'] not in customer_accounts:
            customer_accounts[transaction["customer_id"]] = ba.BankAccount(transaction["customer_id"])
        main_response = customer_accounts[transaction["customer_id"]].load_account(transaction)
        
        if main_response is None:
            pass
        else:
            main_response = json.dumps(main_response, separators=(',', ':'))
            f = open(output_file, "a")
            print(main_response, file=f)
            f.close()



def main(inputs, output_file, text_file=True):

    if text_file == True:
        transactions = load_transactions(inputs)
        process_transactions(transactions, output_file)
    else:
        process_transactions(inputs, output_file)

# main("input.txt", "results.txt")