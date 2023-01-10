import gspread
from databases.databases import *

TOKEN_WORKER = ""
WORKSHEET_NAME = ""

class GoogleSpreadsheetWorker:
    def __init__(self) -> None:
        self.service_account = gspread.service_account(filename=TOKEN_WORKER) 
        self.worksheet = self.service_account.open("WORKSHEET_NAME").sheet1


    def make_order_record(self,order: Order):
        self.worksheet.insert_row([order.id,order.city.name,order.district.name,order.currency.name,order.payment_system.name,order.sum,order.master_id])