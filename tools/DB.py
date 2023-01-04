import sqlite3
import json


class DB():

    # ------------------------------------------------
    def __init__(self, filename):
        self.dbconn = sqlite3.connect(filename)
        self.dbconn.row_factory = sqlite3.Row
        self.setup_tables()

    # ------------------------------------------------
    def setup_tables(self):

        # Somewhere to store the raw transaction data
        self.dbconn.execute('''
            CREATE TABLE IF NOT EXISTS raw_trans (
                transaction_id TEXT UNIQUE NOT NULL,
                account_id TEXT NOT NULL,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                created_at INT NOT NULL,
                updated_at INT NOT NULL,
                jsondata TEXT NOT NULL,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.dbconn.execute('''
            CREATE TABLE IF NOT EXISTS raw_account (
                account_id TEXT NOT NULL,
                name TEXT NOT NULL,
                balance REAL NOT NULL,
                updated_at TEXT NOT NULL,
                jsondata TEXT NOT NULL,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.dbconn.execute('''
            CREATE TABLE IF NOT EXISTS trans_class (
                transaction_id TEXT,
                amount REAL NOT NULL,
                cat1 TEXT,
                cat2 TEXT,
                cat3 TEXT,
                tags TEXT,
                description TEXT,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.dbconn.commit()

    # ------------------------------------------------
    def commit(self):
        return self.dbconn.commit()

    # ------------------------------------------------
    def store_account_data(self, datadict):
        self.dbconn.execute("INSERT INTO raw_account (account_id, name, balance, updated_at, jsondata) VALUES (?,?,?,?,?)",
            [
                datadict["_id"],
                datadict["name"],
                datadict["balance"]["current"],
                datadict["refreshed"]["balance"],
                json.dumps(datadict)
            ]
        )
        self.dbconn.commit()

    # ------------------------------------------------
    def store_transaction_data(self, datadict):
        self.dbconn.execute('''
            INSERT OR REPLACE INTO raw_trans (
                transaction_id,
                account_id,
                date,
                type,
                amount,
                created_at,
                updated_at,
                description,
                jsondata
            ) VALUES (?,?,?,?,?,?,?,?,?)
        ''',
            [
                datadict["_id"],
                datadict["_account"],
                datadict["date"],
                datadict["type"],
                datadict["amount"],
                datadict["created_at"],
                datadict["updated_at"],
                datadict["description"],
                json.dumps(datadict)
            ]
        )
        self.dbconn.commit()

    # ------------------------------------------------
    def get_unclassified_transactions(self, maximum_rows = None):
        #SELECT * FROM raw_trans LEFT JOIN trans_class ON raw_trans.transaction_id = trans_class.transaction_id WHERE trans_class.transaction_id IS NULL
        sql = '''
            SELECT
                raw_trans.transaction_id,
                raw_trans.date,
                raw_trans.type,
                raw_trans.amount,
                raw_trans.description,
                a.name as account,
                json_extract(raw_trans.jsondata, '$.merchant.name') as merchant
            FROM raw_trans
            INNER JOIN (select DISTINCT raw_account.account_id, raw_account.name from raw_account) a ON a.account_id = raw_trans.account_id
            LEFT JOIN trans_class ON raw_trans.transaction_id = trans_class.transaction_id
            WHERE trans_class.transaction_id IS NULL
            ORDER BY raw_trans.date
        '''
        if maximum_rows is not None:
            sql += f" LIMIT {maximum_rows}"

        transactions = self.dbconn.execute(sql)

        return transactions.fetchall()

    # ------------------------------------------------
    def classify_transaction(self, transaction_id, amount, cat1, cat2, cat3, tags, description):
        self.dbconn.execute('''
            INSERT INTO trans_class (
                transaction_id,
                amount,
                cat1,
                cat2,
                cat3,
                tags,
                description
            ) VALUES (?,?,?,?,?,?,?)''',
            [
                transaction_id,
                amount,
                cat1,
                cat2,
                cat3,
                tags,
                description
            ]
        )
        self.dbconn.commit()

    # ------------------------------------------------
    def reclassify_transaction(self, ROWID, amount, cat1, cat2, cat3, tags, description):
        self.dbconn.execute('''
            UPDATE trans_class
            SET amount = ?,
            cat1 = ?,
            cat2 = ?,
            cat3 = ?,
            tags = ?,
            description = ?
            WHERE rowid = ?''',
            [
                amount,
                cat1,
                cat2,
                cat3,
                tags,
                description,
                ROWID
            ]
        )
        self.dbconn.commit()

    # ------------------------------------------------
    def get_suggested_classification(self, merchant, description):
        # have we seen this merchant or description before?
        transactions = self.dbconn.execute('''
            SELECT
                cat1,
                cat2,
                cat3,
                tags,
                trans_class.description
            FROM trans_class
            LEFT JOIN raw_trans ON trans_class.transaction_id = raw_trans.transaction_id
            WHERE json_extract(raw_trans.jsondata, '$.merchant.name') = ? OR raw_trans.description = ?
            ORDER BY trans_class.added_at DESC
            LIMIT 1
            ''',
            [merchant, description]
        )

        data = transactions.fetchone()
        if data is not None:
            return " ".join(item for item in data if item and item.strip())
        else:
            return ""