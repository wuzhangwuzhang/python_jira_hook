import datetime


class Datetools:
    def is_leap_year(self, year):
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            return True
        else:
            return False

    def day_of_year(self, year, month, day):
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        total_days = 0

        for i in range(1, month):
            total_days += days_in_month[i - 1]

        if month > 2 and self.is_leap_year(year):
            total_days += 1

        total_days += day
        return total_days
