import calendar
import datetime
import locale


class CreateDates:
    def __init__(self):
        pass

    # create dates
    def createDates(self, month=datetime.date.today().month, year=datetime.date.today().year):
        # define locale for language month get by calendar.month_name
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # get today date basead in month and year
        self.today  = datetime.date(year, month, 1)

        # get first day of month
        self.firstDayOfMonth = self.today.replace(day=1)

        # get last day of month
        self.lastDayOfMonth = self.today.replace(day=calendar.monthrange(self.today.year, self.today.month)[1])

        # create list of dates
        self.dates = [day.strftime("%d/%m/%Y") for day in (self.firstDayOfMonth + datetime.timedelta(days=day) for day in range((self.lastDayOfMonth - self.firstDayOfMonth).days + 1)) if day.weekday() < 5]

        return self.dates
    
    def defineYears(self):
        # create list of last 2 years and current year
        self.years = [str(year) for year in range(datetime.date.today().year - 2, datetime.date.today().year + 1)]

        return self.years
    
    def defineMonths(self):
        # create list of all months name and number
        self.months = [f"{calendar.month_name[month]} ({str(month).zfill(2)})" for month in range(1, 13)]

        return self.months
    
    def defineActualYear(self):
        # get actual year
        self.actualYear = datetime.date.today().year

        return self.actualYear

    def defineActualMonth(self):
        # get actual month
        self.actualMonth = datetime.date.today().month

        return self.actualMonth
    
    def defineActualDate(self):
        # get actual date
        self.actualDate = datetime.date.today().strftime("%d/%m/%Y")

        return self.actualDate