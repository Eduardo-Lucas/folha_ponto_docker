from datetime import datetime, timedelta
import calendar

def get_previous_month_choices():
    today = datetime.today()
    choices = []

    for i in range(4):
        # Calculate the target month and year
        first_day_of_month = today.replace(day=1)
        target_date = first_day_of_month - timedelta(days=i*30)
        year = target_date.year
        month = target_date.month

        # Get the last day of the month
        last_day = calendar.monthrange(year, month)[1]
        last_day_date = datetime(year, month, last_day)
        formatted_date = last_day_date.strftime('%d/%m/%Y')

        # Add the choice to the list
        choices.append((formatted_date, formatted_date))

    return choices
