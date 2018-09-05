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

initDate = datetime.date(1901, 1, 13)

""" A tuple of years with 27 pay periods"""
yearPPs = (1911, 1922, 1933, 1944, 1956,
            1967, 1978, 1989, 2000, 2012,
            2023, 2034, 2045, 2056, 2067)

def yearStart(initial, target, yearArray):
    """yearStart() calculates the first day of the first pay period of a target
    pay year.

    "initial" must be a datetime.date corrlating to the first day of the first
    pay period of a known year. The initDate global constant is recommended.

    "target" is the target year as an integer.

    "yearArray" is an array (list, tuple, sequence) of years with 27 pay periods.
    """

    initYear = initial.year
    diff = target - initYear
    daysToAdd = 0

    for yr in range(diff):
        if (initYear + yr) in yearArray:
            daysToAdd += 14 * 27
        else: daysToAdd += 14 * 26

    return initial + datetime.timedelta(days = daysToAdd)

def ppStart(yearStart, pp, yearArray):
    """Using the first day of the first pay period of a pay year as a staring
    point, this function returns the start date of the target pay period.
    """

    if pp > 27 or (pp > 26 and yearStart.year not in yearArray):
        # Change to raise PayPeriodError
        return None

    return yearStart + datetime.timedelta(days = (pp - 1) * 14)
