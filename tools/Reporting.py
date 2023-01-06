# This contains reporting stuff for the database

import tools.DB as DB
import tools.date_tools as date_tools

class Reporting():

    # ------------------------------------------------
    def __init__(self, filename):
        self.db = DB.DB(filename)

    # ------------------------------------------------
    def spending_by_tag(self, tag, date_from, date_to):
        
        # tag is a string of tags
        tags = tag.split(' ')
        where = []
        
        for serachlike in tags:
            where.append(f"trans_class.tags LIKE '%{serachlike}%'")

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
        '''
        print(sql)

        transactions = self.db.dbconn.execute(sql)
        return transactions.fetchall()