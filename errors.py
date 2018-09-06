class PayPeriodError(Exception):
    """PayPeriodError is returned any time that the pay period number exceeds
    the number of pay periods in a given year.
    """

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)

class YearUnknownError(Exception):
    """YearUnknownError is raised whenever data about a year is requested and
    it is not found in the year list.
    """

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)
