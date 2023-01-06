# Import the account and transaction data into the database

import tools.DB as DB
import credentials
import requests
import logging
import json
from dateutil import parser as dateutilparser
from datetime import timedelta

database_file = "transactions.sqlite"
bankdb = DB.DB(database_file)
logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)

# -------------------------------------------
def get_accounts():

    url = "https://api.akahu.io/v1/accounts"
    response = requests.request("GET", url, headers=credentials.headers)

    if response.status_code == 200:
        accounts = json.loads(response.text)
        return accounts

    else:
        match response.status_code:
            case 400:
                logger.error("Your request was malformed or otherwise unacceptable. More details are provided under the message key in the response.")
            case 401:
                logger.error("You are not authorised to access this content.")
            case 403:
                logger.error("You are not allowed to access this content.")
            case 500:
                logger.error("An internal error has prevented us from processing the request. More detail may be supplied in the message key.")


# -------------------------------------------
def get_and_store_transactions(startdate_isoformat = None):

    cursor = True

    while cursor:
        if cursor == True:
            if startdate_isoformat is None:
                url = "https://api.akahu.io/v1/transactions"
            else:
                url = f"https://api.akahu.io/v1/transactions?start={startdate_isoformat}"
        else:
            url = "https://api.akahu.io/v1/transactions?cursor="+cursor

        response = requests.request("GET", url, headers=credentials.headers)

        if response.status_code == 200:
            transactions = json.loads(response.text)

            if transactions["success"]:

                cursor = transactions['cursor']['next']
                for transaction in transactions['items']:
                    bankdb.store_transaction_data(transaction)

            else:
                logger.error("Error getting transactions. JSON indicates that data not successful.")
                cursor = False
            
        else:
            print(url)
            cursor = False
            match response.status_code:
                case 400:
                    logger.error("Your request was malformed or otherwise unacceptable. More details are provided under the message key in the response.")
                case 401:
                    logger.error("You are not authorised to access this content.")
                case 403:
                    logger.error("You are not allowed to access this content.")
                case 500:
                    logger.error("An internal error has prevented us from processing the request. More detail may be supplied in the message key.")

# -------------------------------------------
def main():

    data = get_accounts()

    if data is not None and data['success'] == True:
        print("Processing Accounts....")
        for account in data["items"]:

            bankdb.store_account_data(account)

            if account["status"] == "INACTIVE":
                logger.error("There is an account that is INACTIVE. This means that credentials have stopped working.")

    # figure out the newest transaction
    newestdate = bankdb.get_newest_transaction()

    if newestdate is not None:
        # subtract two weeks from the date
        twoweeksago = dateutilparser.parse(newestdate['date']) - timedelta(days=14)
        print(f"Getting transactions from: {twoweeksago}")
        get_and_store_transactions(twoweeksago.isoformat("T","seconds").replace('+00:00', 'Z'))
    else:
        print("Getting all transactions...")
        get_and_store_transactions()










# -------------------------------------------
if __name__ == '__main__':
    main()