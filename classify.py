# Classify the transactions in the database

import tools.DB as DB
import tools.base_classification
# import credentials
# import requests
import logging
import json
import prompt_toolkit
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import NestedCompleter
from tabulate import tabulate
from dateutil import parser as dateutilparser
from dateutil import tz

database_file = "transactions.sqlite"
bankdb = DB.DB(database_file)
logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)

startdate = "2023-01-01"
# startdate = None

# -------------------------------------------
def split_classification(row):
    # Sometimes you have a single purchase that needs to be split up
    
    total_amount = float(row['amount'])
    # update the autocomplete
    completer = NestedCompleter.from_nested_dict(
        bankdb.get_and_update_used_classifications(tools.base_classification.base_classification))
    
    # Have we seen this before?
    defaultclass = bankdb.get_suggested_classification(row['merchant'],row['description'])
    if defaultclass != "":
        print(f"Previous Classification > {defaultclass}")

    # to make this mentally easier, convert everything to positive numbers
    if total_amount > 0:
        signmultiplier = 1
    else:
        total_amount = abs(total_amount)
        signmultiplier = -1

    while total_amount > 0:
        print(f"Splitting Transaction... ${total_amount} remaining")
        amount = float(prompt('Amount > '))

        if amount > total_amount:
            amount = total_amount

        while True:
            # no default as likely to always require a different classification
            classification = prompt('Classification > ', completer=completer, default="")

            match classification:
                case 'x':
                    # exit
                    classified = None
                    total_amount = 0
                    break
                case 'q':
                    quit()

            # classification now contains the classification data. Need to parse this and split out
            classified = parse_classification(classification)

            # validate
            validinput = check_parse_classification(classified)
            if not validinput:
                print("Something looks funky with that classification")
                print(classified)
                print("Please try again")
            else:
                break

        # Now push this into the database
        if classified is not None:
            bankdb.classify_transaction(
                row['transaction_id'],
                amount * signmultiplier,
                classified['cat1'],
                classified['cat2'],
                classified['cat3'],
                " ".join(classified['tags']),
                classified['description']
            )

        # subtract this amount from the total
        total_amount -= amount


# -------------------------------------------
def check_parse_classification(classified):
    # do a sanity check
    if classified['cat1'] is None: return False
    if len(classified['cat1']) < 3: return False
    if classified['cat2'] is not None and len(classified['cat2']) < 2: return False
    if classified['cat3'] is not None and len(classified['cat3']) < 2: return False
    return True


# -------------------------------------------
def parse_classification(classification):

    classified = {
        'cat1': None,
        'cat2': None,
        'cat3': None,
        'tags': set(),
        'description': None
    }
    catcomplete = False
    tagcomplete = False
    # this is space separated text
    # cat1 cat2 cat3 #tags description

    # this stupid split and combine is to remove any additional double spaces just in case
    items = " ".join(classification.split(' ')).split(' ')

    for i, item in enumerate(items):
        if i <= 2 and not item.startswith("#") and not catcomplete:
            match i:
                case 0:
                    classified['cat1'] = item.lower()
                    continue
                case 1:
                    classified['cat2'] = item.lower()
                    continue
                case 2:
                    classified['cat3'] = item.lower()
                    catcomplete = True
                    continue

        if not tagcomplete and item.startswith("#"):
            classified['tags'].add(item.lower())
            catcomplete = True
            continue

        if not item.startswith("#") and catcomplete:
            tagcomplete = True
            classified['description'] = item if classified['description'] is None else " ".join([classified['description'],item])

    return classified


# -------------------------------------------
def pretty_print_transaction(row):
    prompt_toolkit.shortcuts.clear()

    # convert the UTC date to local
    thedate = dateutilparser.parse(row['date'])
    thedate.replace(tzinfo=tz.tzutc())
    thedate = thedate.astimezone(tz.tzlocal())

    table = [
        ['Date', thedate.strftime("%Y-%m-%d %H:%M:%S (%A)")],
        ['Description', row['description']],
        ['Merchant', row['merchant']],
        ['Account', row['account']],
        ['Type', row['type']],
        ['Amount', row['amount']],
    ]
    print('Ctrl-U = clear line')
    print(tabulate(table, tablefmt='fancy_grid'))


# -------------------------------------------
def main():

    rows = bankdb.get_unclassified_transactions(None, startdate)
    print(f"{len(rows)} transactions to classify")

    for row in rows:
        
        pretty_print_transaction(row)

        # update the autocomplete
        completer = NestedCompleter.from_nested_dict(
            bankdb.get_and_update_used_classifications(tools.base_classification.base_classification))

        while True:

            # Have we seen this before?
            defaultclass = bankdb.get_suggested_classification(row['merchant'],row['description'])

            # Did this come from a personal spending account?
            if 'bernadette' in row['account'].lower():
                if '#bernadette' not in defaultclass:
                    defaultclass += " #bernadette"

            if 'nick' in row['account'].lower():
                if '#nick' not in defaultclass:
                    defaultclass += " #nick"
            
            classification = prompt('Classification > ', completer=completer, default=defaultclass)

            # There are a couple of special commands that we need to check the input for
            # s = user has asked to split this transaction into two (or more) classifications
            # x = user has asked to skip this row and come back to it later.

            match classification:
                case 'x':
                    # skip
                    classified = None
                    break
                case 'q':
                    quit()
                case 's':
                    # split the transaction. This does its own database addition
                    # so set classified to None and break out of the loop to get to
                    # the next row to process.
                    split_classification(row)
                    classified = None
                    break
                case 'm':
                    # Display more details about the transaction
                    print(json.dumps(json.loads(row['jsondata']),sort_keys=True, indent=4))


            # classification now contains the classification data. Need to parse this
            # and split out
            classified = parse_classification(classification)

            # validate
            validinput = check_parse_classification(classified)
            if not validinput:
                print("Something looks funky with that classification")
                print(classified)
                print("Please try again")
            else:
                break

        # Now push this into the database
        if classified is not None:
            bankdb.classify_transaction(
                row['transaction_id'],
                row['amount'],
                classified['cat1'],
                classified['cat2'],
                classified['cat3'],
                " ".join(classified['tags']),
                classified['description']
            )
            


# -------------------------------------------
if __name__ == '__main__':
    main()