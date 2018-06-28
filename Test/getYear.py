import re
import datetime

def FindURL(dob):
    new = int(re.sub(r".*(\d{4}).*", r"\1", dob))
    return new


now = datetime.datetime.now()
age=now.year-FindURL("1/66/1992")
print(age)