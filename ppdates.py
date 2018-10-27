"""
Fedpp provides functions and classes to calculate biweekly pay period dates in
the federal pay system. The system dates back to 1900 Jan 01. Each pay period
begins on a Sunday and ends on the Saturday of the following week. Each year in
the pay calendar is 26 pay periods long (52 weeks or 364 days).

Due to a 1.25 day discrepancy between the pay calendar and Gregorian calendar,
The federal pay system incorporates a 27th pay period every 11.2 years to
account for this discrepancy. Because 11.2 does not evenly divide into any given
year, it occurs five times over the course of 56 years in the following pattern:

Year 1 - 10:    26 pay periods
Year 11:        27 pay periods
Year 12 - 21    26 pay periods
Year 22:        27 pay periods
Year 23 - 32    26 pay periods
Year 33:        27 pay periods
Year 34 - 43    26 pay periods
Year 44:        27 pay periods
Year 45 - 55    26 pay periods
Year 56:        27 pay periods

At the end of the 56th year, the cycle resets and begins anew.
"""

import datetime
import github.SMTullis.ppdates.errors as errors

INIT_DATE = datetime.date(1901, 1, 13)

YEARS_WITH_27PPS = (
    1911, 1922, 1933, 1944, 1956,
    1967, 1978, 1989, 2000, 2012,
    2023, 2034, 2045, 2056, 2068,
    2079, 2090, 2101, 2112, 2124
)

class PayCalendar:
    initial_date = None
    year_tuple = ()

    def __init__(self, initial_date, year_tuple):
        self.initial_date = initial_date
        self.year_tuple = year_tuple

    def calc_days_to_add(self, year):
        days_to_add = self.calc_days_in_completed_cycles(year)
        start_date = self.initial_date + datetime.timedelta(days = days_to_add)
        initial_year = start_date.year

        for yr in range(year - initial_year):
            days_to_add += (14 * self.calc_pay_periods_in_year(initial_year + yr))

        return days_to_add

    def calc_days_in_completed_cycles(self, year):
        return ((year - self.initial_date.year) // 56) * 20454

    def calc_pay_periods_in_year(self, year):
        if year in self.year_tuple:
            return 27

        return 26

    def calc_pay_period_number(self, year_start_date, target_date):
        pay_period_no = calc_completed_pay_periods(
            calc_days_between(target_date, year_start_date)
        ) + 1

        if not self.is_pay_period_in_range(year_start_date.year, pay_period_no):
            raise errors.PayPeriodError

        return pay_period_no

    def is_pay_period_in_range(self, year, pay_period_no):
        if 1 <= pay_period_no <= self.calc_pay_periods_in_year(year) :
            return True

        return False

    def calc_pay_period_start_date(self, year_start_date, pay_period_no):
        if not self.is_pay_period_in_range(year_start_date.year, pay_period_no):
            raise errors.PayPeriodError

        return year_start_date + datetime.timedelta(days = (pay_period_no - 1) * 14)

    def calc_pay_period_start_date_by_date(self, year_start_date, target_date):
        number = self.calc_pay_period_number(year_start_date, target_date)
        return self.calc_pay_period_start_date(year_start_date, number)

    def calc_years_since_initial_date(self, target_year):
        return target_year - self.initial_date.year

    def calc_year_start_date(self, year):
        if not self.is_year_in_range(year):
            raise errors.YearUnknownError(year)

        return self.initial_date + datetime.timedelta(days = self.calc_days_to_add(year))

    def is_year_in_range(self, year):
        if min(self.year_tuple) - 10 <= year <= max(self.year_tuple) + 10:
            return True

        return False

    def generate_pay_period_range(self, start_date, endDate):
        year = self.calc_year_start_date(start_date.year)
        start = self.calc_pay_period_start_date(year, self.calc_pay_period_number(year, start_date))

        year = self.calc_year_start_date(endDate.year)
        end = self.calc_pay_period_start_date(year, self.calc_pay_period_number(year, endDate))

        pay_periods = ((end.toordinal() - start.toordinal()) // 14) +1

        return [start + datetime.timedelta(days = 14 * pp) for pp in range(pay_periods)]

    def generate_year_calendar(self, year):
        return PayYear(year, self.calc_year_start_date(year), self.calc_pay_periods_in_year(year))

class PayYear:
    year = 0
    year_start_date = None
    total_pay_periods = 0
    pay_period_list = []

    def __init__(self, year, year_start_date, total_pay_periods):
        self.year = year
        self.year_start_date = year_start_date
        self.total_pay_periods = total_pay_periods

    def generate_pay_period_list(self):
        self.pay_period_list = [PayPeriod(number + 1,
            self.year_start_date + datetime.timedelta(days = 14 * number))
            for number in range(self.total_pay_periods)
        ]

class PayPeriod:
    id_no = 0
    start_date = None
    date_list = [
        [],
        []
    ]

    def __init__(self, id_no, start_date):
        self.id_no = id_no
        self.start_date = start_date

    def generate_date_list(self):
        self.date_list[0] = [
            self.start_date + datetime.timedelta(days = offset) \
            for offset in range(7)
        ]
        self.date_list[1] = [
            self.start_date + datetime.timedelta(days = offset + 7) \
            for offset in range(7)
        ]

def calc_days_between(earlier, later):
    return later.toordinal() - earlier.toordinal()

def calc_completed_pay_periods(days):
    return days // 14
