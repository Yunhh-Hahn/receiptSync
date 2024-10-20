from OCR_endSum import getTotalValue
import datetime
import gspread
from google.oauth2.service_account import Credentials

def getDateTimeobject(date: str) -> object:
    format = '%d/%m/%Y'
    dateObject = datetime.datetime.strptime(date, format)
    return dateObject

def getSheet_dayFormat(date: object) -> object:
    return date.strftime("%d/%m/%Y")

def lenColumn(worksheet: object):
    colList = worksheet.col_values(1)
    colLength = len(colList)
    return colLength

# def isNextWeek() -> bool:
#     today = getToday()
#     sheetWeek = getLast_budgetDay(worksheet)

#     return (getDateTimeobject(today) > getDateTimeobject(sheetWeek))

# def getToday():
#     date = datetime.datetime.today()
#     return getSheet_dayFormat(date)

# Why did I do this, there is method that allow for me to get the value of only a single cell, in this shit, 
# I have querried the entire column twice already ???
def getBudgetWeek(worksheet: object)-> str:
    dateCell = worksheet.find("Date")
    colLength = lenColumn(worksheet)

    week = worksheet.cell(dateCell.row, colLength)
    return week

def getLast_budgetDay(worksheet: object)-> str :
    week = getBudgetWeek(worksheet)
    lastDay = week[13:]
    return lastDay

def getNext_lastDay(startDay: object) -> object:
    lastDay = startDay + datetime.timedelta(days=6)
    return lastDay

def insertBudgetWeek(worksheet: object) -> None:
    colLength = lenColumn(worksheet)

    lastWeek_Day = getLast_budgetDay(worksheet)
    startDay = getDateTimeobject(lastWeek_Day) + datetime.timedelta(days=1)
    # A week have 7 day with the start day being 1 so plus 6 to get lastday
    lastDay = getNext_lastDay(startDay)
    weekRange = getSheet_dayFormat(startDay) + " - " + getSheet_dayFormat(lastDay)

    worksheet.update_acell(f"A{colLength + 1}", weekRange)


def insertReceipt(worksheet: object, receiptTotal: float)-> None :
    colLength = lenColumn(worksheet)
    # today = getToday()
    # week = getLast_budgetDay(worksheet)

    # if ((getDateTimeobject(today) <= getDateTimeobject(week)) == True):
    if (isNextWeek() == False):
        val = worksheet.acell(f"J{colLength}").value
        if val == None:
            val = 0

        newVal = float(val) + receiptTotal   
        worksheet.update_acell(f"J{colLength}", newVal)
    else:
        worksheet.update_acell(f"J{colLength + 1}", receiptTotal)


class Receipt:
    def __init__(self, total) -> None:
        self.total = total
    def __repr__(self) -> str:
        return(f"Receipt(total={self.total})")


class ExpenseManager:
    def __init__(self, worksheet, receipt: Receipt, rent: int, phonePlan: int, others) -> None:
        self.worksheet = worksheet
        self.rent = rent
        self.receipt = receipt
        self.phonePlan = phonePlan
        self.others = others
        self.today = datetime.today()
    def insertBugdetWeek():
        today = datetime.today()

        dateCell = worksheet.find("Date")
        colLength = lenColumn(worksheet)
        week = worksheet.cell(dateCell.row, colLength)
        lastDay = week[13:]
    

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("./credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1H0AkwmjPrj0Q0DpDpuxJtzV7bpWVR5rhXFZzYnrlUzg"
sheet = client.open_by_key(sheet_id)

worksheet = sheet.worksheet("Sheet1")

photoPath = "20241007_230638.jpg"
receiptTotal = getTotalValue(photoPath)

if (isNextWeek() == True):
    insertBudgetWeek(worksheet)
insertReceipt(worksheet= worksheet, receiptTotal= receiptTotal)
