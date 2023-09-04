import datetime

# Get the current month to know which sheet to access in the Google Spreadsheet


def current_month():
    today = datetime.date.today()
    month = today.strftime("%B")
    return month
