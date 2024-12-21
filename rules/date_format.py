from datetime import datetime
from . import Rule

class DateFormat(Rule):
    def __init__(self, format):
        self.format = format

    def passes(self, attribute, value, parameters, validator):
        try:
            datetime.strptime(value, self.format)
            return True
        except ValueError:
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} does not match the format {self.format}."