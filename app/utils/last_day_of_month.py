import calendar
from datetime import datetime

def get_last_day_of_month(date):
    """Return the last day of the month for a given date."""
    year = date.year
    month = date.month
    _, last_day = calendar.monthrange(year, month)
    return last_day
