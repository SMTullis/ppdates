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
