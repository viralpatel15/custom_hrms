import frappe
from frappe import _
from frappe.utils import getdate
from erpnext.accounts.utils import get_fiscal_year

def validate(self, method):
    posting_month = getdate(self.posting_date).month
    fiscal_year =  get_fiscal_year(self.posting_date, as_dict=True)
    month = {
            1:'JAN',
            2:'FEB',
            3:'MARCH',
            4:'APRIL',
            5:'MAY',
            6:'JUN',
            7:'JULY',
            8:'AUG',
            9:'SEP',
            10:'OCT',
            11:'NOV',
            12:'DEC'
    }
    month = month.get(posting_month)
    data = frappe.db.sql(f"""Select name, sum(overtime_days) as overtime_days, sum(lunch) as lunch
                            From `tabMonthly Overtime`
                            where year = '{fiscal_year.name}' and month = '{month}' and employee = '{self.employee}'
                            Group By employee
                        """, as_dict = 1)
    
    if data:
        self.custom_overtimedays = data[0].overtime_days
        self.custom_lunch = data[0].lunch