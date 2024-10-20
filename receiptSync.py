from OCR_endSum import getTotalValue
import datetime
import gspread
import calendar
from google.oauth2.service_account import Credentials



def lenColumn(worksheet: object):
    colList = worksheet.col_values(1)
    colLength = len(colList)
    return colLength

# def insertReceipt(worksheet: object, receiptTotal: float)-> None :
#     colLength = lenColumn(worksheet)
#     # today = getToday()
#     # week = getLast_budgetDay(worksheet)

#     # if ((getDateTimeobject(today) <= getDateTimeobject(week)) == True):
#     if (isNextWeek() == False):
#         val = worksheet.acell(f"J{colLength}").value
#         if val == None:
#             val = 0

#         newVal = float(val) + receiptTotal   
#         worksheet.update_acell(f"J{colLength}", newVal)
#     else:
#         worksheet.update_acell(f"J{colLength + 1}", receiptTotal)


class Receipt:
    def __init__(self, total) -> None:
        self.total = total
    def __repr__(self) -> str:
        return(f"Receipt(total={self.total})")


class ExpenseManager:
    def __init__(self, worksheet, receipt: Receipt, rent: int, phonePlan: int, others, time_format = "%d/%m/%Y") -> None:
        self.worksheet = worksheet
        self.rent = rent
        self.receipt = receipt
        self.phonePlan = phonePlan
        self.others = others
        self.time_format = time_format

    def getDateTimeobject(self, date: str) -> object:
        dateObject = datetime.datetime.strptime(date, self.time_format)
        return dateObject
    
    def getSheet_timeFormat(self, date: datetime) -> str:
        return date.strftime(self.time_format)

    def insertBugdetWeek(self):
        today = datetime.today()

        dateCell = worksheet.find("Date")
        colLength = lenColumn(worksheet)
        week = worksheet.cell(dateCell.row, colLength)
        lastSheetDay = self.getDateTimeobject(week[13:])

        if (today > lastSheetDay):
            startDay = lastSheetDay +  datetime.timedelta(days=1)
            endDay = startDay + datetime.timedelta(days=6)
            # Edge case: Last day of recording to the sheet is more than 1 weeks behind
            while(today > endDay):
                startDay = startDay + datetime.timedelta(days=7)
                endDay = endDay + datetime.timedelta(days=7)
            
        weekRange = self.getSheet_timeFormat(startDay) + " - " + self.getSheet_timeFormat(endDay)
        self.worksheet.update_cell(dateCell.row,colLength, weekRange)
    

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("./credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1H0AkwmjPrj0Q0DpDpuxJtzV7bpWVR5rhXFZzYnrlUzg"
sheet = client.open_by_key(sheet_id)

worksheet = sheet.worksheet("Sheet1")

photoPath = "20241007_230638.jpg"
receiptTotal = getTotalValue(photoPath)


