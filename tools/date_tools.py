# some tools to convert dates to UTC

from datetime import datetime   
from dateutil import tz

def convert_date_to_beginning_of_day_UTC_isoformat(date_string):
    return _convert_date_to_UTC_isoformat(date_string, "00:00:01")

def convert_date_to_end_of_day_UTC_isoformat(date_string):
    return _convert_date_to_UTC_isoformat(date_string, "23:59:59")

def _convert_date_to_UTC_isoformat(date_string, time_string):
    datetime_string = date_string + " " + time_string
    datetime_object = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    datetime_object.replace(tzinfo=tz.tzlocal())
    datetime_object = datetime_object.astimezone(tz.tzutc())
    return datetime_object.isoformat().replace('+00:00', 'Z')



# -------------------------------------------
if __name__ == '__main__':
    
    testdate2 = "2023-01-07"
    testdate1 = "2023-01-01"

    print(convert_date_to_beginning_of_day_UTC_isoformat(testdate1))
    print(convert_date_to_end_of_day_UTC_isoformat(testdate1))
    print()
    print(convert_date_to_beginning_of_day_UTC_isoformat(testdate2))
    print(convert_date_to_end_of_day_UTC_isoformat(testdate2))