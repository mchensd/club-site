from django.core.exceptions import ValidationError
import datetime as dt
def validate_date_time(s):
    try:
        print(s)
        dt.datetime.strptime(s, "%m-%d-%Y")
    except:
        print("Bad Date")
        raise ValidationError("Please enter date in the format MM-DD-YYYY")
