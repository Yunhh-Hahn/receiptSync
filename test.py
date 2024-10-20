import datetime
import calendar

def getToday():
    date = datetime.datetime.today()
    return date.strftime("%d/%m/%Y")

def getDateTimeobject(date: str) -> object:
    format = '%d/%m/%Y'
    dateObject = datetime.datetime.strptime(date, format)
    return dateObject

date = getToday()
print(date)
print(getDateTimeobject(date))
date = getDateTimeobject(date) + datetime.timedelta(days=7)
print(date)

string = "01/10/2024 - 07/10/2024"
print(string[13:])

print(calendar.monthrange(2024,10))