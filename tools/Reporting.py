# This contains reporting stuff for the database

import tools.DB as DB
import tools.date_tools as date_tools
from typing import List
import sqlite3

ignore_account1 = 'acc_clccx4vex000308l3fttlelqx'

class Reporting():

    # ------------------------------------------------
    def __init__(self, filename):
        self.db = DB.DB(filename)

    # ------------------------------------------------
    def spending_by_tag(self, date_from, date_to, tag):
        
        # tag is a string of tags
        tags = tag.split(' ')
        where = []
        
        for searchlike in tags:
            where.append(f"trans_class.tags LIKE '%{searchlike}%'")

        sql = f'''
            SELECT 
                raw_trans.description,
                trans_class.amount,
                trans_class.cat1,
                trans_class.cat2,
                trans_class.cat3,
                trans_class.tags,
                trans_class.description
            FROM trans_class 
            LEFT JOIN raw_trans ON trans_class.transaction_id = raw_trans.transaction_id
            WHERE
                ({" OR ".join(where)})
            AND
                raw_trans.date >= '{date_tools.convert_date_to_beginning_of_day_UTC_isoformat(date_from)}'
            AND
                raw_trans.date <= '{date_tools.convert_date_to_end_of_day_UTC_isoformat(date_to)}'
            AND
                raw_trans.account_id != '{ignore_account1}'
            ORDER BY
                trans_class.cat1, trans_class.cat2, trans_class.cat3
        '''
        # print(sql)

        transactions = self.db.dbconn.execute(sql)
        return transactions.fetchall()

    # ------------------------------------------------
    def sum_amount(self, rows):
        amount = 0
        for row in rows:
            amount += row['amount']
        return amount

    # ------------------------------------------------
    def spending_by_cat1(self, date_from, date_to, ignore_cat = "", include_cat = ""):
        
        ignore_cat = ignore_cat.split(' ')
        ignore_where = []
        if ignore_cat[0] != '':
            for whereitem in ignore_cat:
                ignore_where.append(f"cat1 <> '{whereitem}'")

        include_cat = include_cat.split(' ')
        include_where = []
        if include_cat[0] != '':
            for whereitem in include_cat:
                include_where.append(f"cat1 == '{whereitem}'")

        sql = f'''
        SELECT cat1, SUM(trans_class.amount) as amount
        FROM trans_class
        LEFT JOIN raw_trans ON trans_class.transaction_id = raw_trans.transaction_id
        WHERE
            raw_trans.date >= '{date_tools.convert_date_to_beginning_of_day_UTC_isoformat(date_from)}'
        AND
            raw_trans.date <= '{date_tools.convert_date_to_end_of_day_UTC_isoformat(date_to)}'
        AND
                raw_trans.account_id != '{ignore_account1}'
        '''
        
        if len(ignore_where) > 0:
            sql += " AND " + " AND ".join(ignore_where)

        if len(include_where) > 0:
            sql += " AND " + " AND ".join(include_where)
            
        sql += " GROUP BY cat1 ORDER BY cat1"
        #print(sql)
        transactions = self.db.dbconn.execute(sql)
        return transactions.fetchall()

    # ------------------------------------------------
    def spending_by_cat2(self, date_from, date_to, ignore_cat = ""):
        
        ignore_cat = ignore_cat.split(' ')
        where = []
        for whereitem in ignore_cat:
            where.append(f"cat1 <> '{whereitem}'")

        sql = f'''SELECT cat1, cat2, SUM(trans_class.amount) as amount
        FROM trans_class
        LEFT JOIN raw_trans ON trans_class.transaction_id = raw_trans.transaction_id
        WHERE
            raw_trans.date >= '{date_tools.convert_date_to_beginning_of_day_UTC_isoformat(date_from)}'
        AND
            raw_trans.date <= '{date_tools.convert_date_to_end_of_day_UTC_isoformat(date_to)}'
        AND
                raw_trans.account_id != '{ignore_account1}'
        '''

        if len(where) > 0:
            sql += " AND " + " AND ".join(where)
        sql += " GROUP BY cat1, cat2 ORDER BY cat1, cat2"
        
        transactions = self.db.dbconn.execute(sql)
        return transactions.fetchall()

    # ------------------------------------------------
    def income(self, date_from, date_to):
        # why did I do it like this?
        # allcat = self.spending_by_cat1(date_from, date_to)

        # exclude = []
        # for row in allcat:
        #     print(row['cat1'])
        #     if row['cat1'] != 'income' and row['cat1'] != 'transfer':
        #         exclude.append(row['cat1'])
        
        # print(exclude)

        return self.spending_by_cat1(date_from, date_to, include_cat='income')

    # ------------------------------------------------
    def spend(self, date_from, date_to):
        # why did I do it like this?
        # allcat = self.spending_by_cat1(date_from, date_to)

        exclude = 'income transfer work'
        spend = self.spending_by_cat1(date_from, date_to, ignore_cat=exclude)
        spendamount = 0
        for row in spend:
            spendamount += row['amount']

        return [{'cat1':'spend','amount':spendamount}]
    
    # ------------------------------------------------
    def work_expenses(self, date_from: str, date_to: str) -> List[sqlite3.Row]:
        """Returns the outstanding work expenses, grouped by cat3

        Args:
            date_from (str): Date in YYYY-MM-DD format
            date_to (str): Date in YYYY-MM-DD format

        Returns:
            list: A list of sql.rows
        """
        
        sql = f'''select cat3, sum(trans_class.amount) as amount
        FROM trans_class
        LEFT JOIN raw_trans ON trans_class.transaction_id = raw_trans.transaction_id
        WHERE
            raw_trans.date >= '{date_tools.convert_date_to_beginning_of_day_UTC_isoformat(date_from)}'
        AND
            raw_trans.date <= '{date_tools.convert_date_to_end_of_day_UTC_isoformat(date_to)}'
        AND
            cat1 = 'work'
        AND
            cat2 = 'expense_claim' 
        GROUP BY
            cat3
        '''
        
        transactions = self.db.dbconn.execute(sql)
        return transactions.fetchall()