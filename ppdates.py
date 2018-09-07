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
import errors

INITDATE = datetime.date(1901, 1, 13)

YEARSWITH27PPS = (1911, 1922, 1933, 1944, 1956,
                1967, 1978, 1989, 2000, 2012,
                2023, 2034, 2045, 2056, 2068,
                2079, 2090, 2101, 2112, 2124)

class PayCalendar:
    initialDate = None
    yearList = ()

    def __init__(self, initialDate, yearList):
        self.initialDate = initialDate
        self.yearList = yearList

    def checkYearInRange(year):
        if year > max(self.yearList) + 10 or year < min(self.yearList) - 10:
            return false

        return true

    def calcDaysToAdd(year):
        daysToAdd = calcTranspiredDays(year)
        startDate = self.initialDate + datetime.timedelta(days = daysToAdd)
        initYear = startDate.year
        diff = year - initYear

        for yr in range(diff):
            if (initYear + yr) in self.yearList:
                daysToAdd += 14 * 27
            else: daysToAdd += 14 * 26

        return daysToAdd

    def calcTranspiredDays(year):
        # To reduce the number of loop iterations below, update the initialDate
        # by the number of days in the 56-year cycle for the number of cycles that
        # have transpired. Using floor division to divide the year difference by
        # 56 provides the number of complete, transpired cycles.
        return ((year - self.initialDate.year) // 56) * 20454

    def calcYearStartDate(year):
        """calcYearStartDate() calculates the first day of the first pay period
        of a target pay year.
        """

        if not checkYearInRange(year):
            raise errors.YearUnkownError(
                "{} is not available.".format(year)
            )

        return self.initialDate + datetime.timedelta(days = calcDaysToAdd(year))

    def calcPPStartDate(yearStartDate, payPeriodNo):
        """Using the first day of the first pay period of a pay year as a staring
        point, this function returns the start date of the target pay period.
        """

        payPeriodsInYear = calcPayPeriodsInYear(yearStartDate.year)

        if payPeriodNo > payPeriodsInYear:
            raise errors.PayPeriodError(
                "{year} only has {pp} pay periods.".format(
                year = yearStartDate.year, pp = payPeriodsInYear
                )
            )

        return yearStartDate + datetime.timedelta(days = (payPeriod - 1) * 14)

    def calcPPNumber(yearStartDate, targetDate):
        """calcPPNumber returns the number of a pay period given the start date. To
        accomplish this, we determine the number of days between the dates and
        divide by the number of days in each pay period, 14. Moreover, using floor
        division ensures that we return the integer value.
        """

        payPeriodNo = ((targetDate.toordinal() - yearStartDate.toordinal()) // 14) + 1

        payPeriodsInYear = calcPayPeriodsInYear(yearStartDate.year)

        if payPeriodNo > payPeriodsInYear or payPeriodNo < 1:
            raise errors.PayPeriodError(
                "Target pay period is not in the given pay year."
            )

        return payPeriodNo

    def findPPInfo(targetDate):
        """findPPInfo returns the pay year, pay period number, and pay period start
        date applicable to the target date.
        """

        proposedDate = calcYearStartDate(targetDate.year)

        if targetDate < proposedDate:
            proposedDate = calcYearStartDate(targetDate.year - 1)

        payPeriodNo = calcPPNumber(proposedDate, targetDate)
        payPeriodDate = calcPPStartDate(proposedDate, payPeriodNo)

        return proposedDate.year, payPeriodNo, payPeriodDate

    def calcPayPeriodsInYear(year):
        if year in self.yearList:
            payPeriodsInYear = 27
        else: payPeriodsInYear = 26

        return payPeriodsInYear

    def yearsSinceInitialDate(targetYear):
        return targetYear - self.initialDate.year
