# This is used to provide a list of classifications

import tools.base_classification
import tools.DB as DB
import json

def formatData(t,s):
    if not isinstance(t,dict) and not isinstance(t,list):
        if t is not None:
            print("   "*s+str(t))
    else:
        for key in t:
            print("   "*s+str(key))
            if not isinstance(t,list):
                formatData(t[key],s+1)


database_file = "transactions.sqlite"
bankdb = DB.DB(database_file)

# print(json.dumps(tools.base_classification.base_classification,sort_keys=True, indent=4))

newcla = bankdb.get_and_update_used_classifications(tools.base_classification.base_classification)

print(json.dumps(newcla, indent=4))

formatData(newcla,0)
