# BigSpender

Basic budget tracking tool on the command line.

Imports the bank transactions via Akahu and stores them into a SQLite database.

Allows you to classify the transactions and then report on the results.

## Setup

You will need to signup for a Akahu developer account and connect your bank details up. Edit the `credentials.py` file and add your Akahu credentials.

Edit the `base_classification.py` to setup your initial budget categories (you can override these as you use `classify.py` if you don't have it perfect from the start)

## Usage

### Import Data

Run `import.py` to create and import the Account and Transaction data. This is pretty basic - it grabs the current account balances and stores this in the `raw_account` table and then grabs the raw transaction data and stores it in the `raw_trans` table. On each run, only transactions two weeks older than then latest data is imported (this is just so pending transactions that might take a while to clear with the bank are not missed)

### Classify Data

Run `classify.py` to classify the transactions.

For each unclassifed transaction you can give it up to three categories, then an unlimited number of tags and a description (note that if using a description then at least one tag is mandatory). You just enter this as text in the format `cat1 cat2 cat3 #tag1 #tag2 Description`

The classification prompt does Autocomplete based on the `base_classification.py` as well as any additional categories added to the database.

If a transaction like this has been seen before, the default text will be populated with the previous classification.

When performing classification there are a couple of commands can be used - `x` will skip this transaction, `q` will quit, `m` will show more details about the transaction and `s` will split the transaction.

Split transactions allow you to split the amount in the transaction between multiple categories (eg when doing food shopping, you could split the __food__ from the __cleaning__ items)

### Reporting

Todo - still need to decided how to show. Jupyter Notebook?