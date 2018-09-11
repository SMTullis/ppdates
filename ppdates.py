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
import custom.ppdates.errors

INITDATE = datetime.date(1901, 1, 13)

YEARSWITH27PPS = (1911, 1922, 1933, 1944, 1956,
                1967, 1978, 1989, 2000, 2012,
                2023, 2034, 2045, 2056, 2068,
                2079, 2090, 2101, 2112, 2124)

class PayCalendar:
    initialDate = None
    yearTuple = ()

    def __init__(self, initialDate, yearTuple):
        self.initialDate = initialDate
        self.yearTuple = yearTuple

    def calcDaysToAdd(self, year):
        daysToAdd = self.calcDaysInCompletedCycles(year)
        startDate = self.initialDate + datetime.timedelta(days = daysToAdd)
        initYear = startDate.year

        for yr in range(year - initYear):
            daysToAdd += (14 * self.calcPayPeriodsInYear(initYear + yr))

        return daysToAdd

    def calcDaysInCompletedCycles(self, year):
        """To reduce the number of loop iterations below, update the initialDate
        by the number of days in the 56-year cycle for the number of cycles that
        have transpired. Using floor division to divide the year difference by
        56 provides the number of complete, transpired cycles.
        """
        return ((year - self.initialDate.year) // 56) * 20454

    def calcPayPeriodsInYear(self, year):
        if year in self.yearTuple:
            return 27

        return 26

    def calcPPNumber(self, yearStartDate, targetDate):
        payPeriodNo = ((targetDate.toordinal() - yearStartDate.toordinal()) // 14) + 1

        if not self.checkPPInRange(yearStartDate.year, payPeriodNo):
            raise errors.PayPeriodError

        return payPeriodNo

    def checkPPInRange(self, year, payPeriodNo):
        if 1 <= payPeriodNo <= self.calcPayPeriodsInYear(year) :
            return True

        return False

    def calcPPStartDate(self, yearStartDate, payPeriodNo):
        if not self.checkPPInRange(yearStartDate.year, payPeriodNo):
            raise errors.PayPeriodError

        return yearStartDate + datetime.timedelta(days = (payPeriodNo - 1) * 14)

    def calcYearsSinceInitialDate(self, targetYear):
        return targetYear - self.initialDate.year

    def calcYearStartDate(self, year):
        if not self.checkYearInRange(year):
            raise errors.YearUnknownError(year)

        return self.initialDate + datetime.timedelta(days = self.calcDaysToAdd(year))

    def checkYearInRange(self, year):
        if min(self.yearTuple) - 10 <= year <= max(self.yearTuple) + 10:
            return True

        return False

    def generateYearCalendar(self, year):
        return PayYear(year, self.calcYearStartDate(year), self.calcPayPeriodsInYear(year))

class PayYear:
    year = 0
    yearStartDate = None
    totalPayPeriods = 0
    payPeriodList = []

    def __init__(self, year, yearStartDate, totalPayPeriods):
        self.year = year
        self.yearStartDate = yearStartDate
        self.totalPayPeriods = totalPayPeriods

    def generatePayPeriodList(self):
        self.payPeriodList = [PayPeriod(number + 1,
            self.yearStartDate + datetime.timedelta(days = 14 * number))
            for number in range(self.totalPayPeriods)]

class PayPeriod:
    payPeriodNo = 0
    payPeriodStartDate = None
    dateList = [
        [],
        []
    ]

    def __init__(self, payPeriodNo, payPeriodStartDate):
        self.payPeriodNo = payPeriodNo
        self.payPeriodStartDate = payPeriodStartDate

    def generateDateList(self):
        self.dateList[0] = [
            self.payPeriodStartDate + datetime.timedelta(days = offset) \
            for offset in range(7)
        ]
        self.dateList[1] = [
            self.payPeriodStartDate + datetime.timedelta(days = offset + 7) \
            for offset in range(7)
        ]
