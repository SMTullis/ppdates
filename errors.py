class RangeError(Exception):
    pass

class PayPeriodError(RangeError):
    """PayPeriodError is returned any time that the pay period number exceeds
    the number of pay periods in a given year.
    """

    errorText = "Target pay period is not in the given pay year."

    def __init__(self):
        pass

    def __str__(self):
        return repr(self.errorText)

class YearUnknownError(RangeError):
    """YearUnknownError is raised whenever data about a year is requested and
    it is not found in the year list.
    """

    error = "{} is not available."
    year = 0

    def __init__(self, year):
        self.year = year

    def __str__(self):
        return repr(self.error.format(self.year))
