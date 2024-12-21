from datetime import datetime
from . import Rule

class DateEquals(Rule):
    def __init__(self, date):
        self.date = date

    def passes(self, attribute, value, parameters, validator):
        try:
            date_format = validator.rules.get(self.date)[0][1][0]
            compare_date = datetime.strptime(validator.data.get(self.date), date_format)
            current_date = datetime.strptime(value, date_format)
            return current_date == compare_date
        except (ValueError, TypeError):
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be equal to {self.date}."