from datetime import datetime
from . import Rule

class Date(Rule):
    def passes(self, attribute, value, parameters, validator):
        try:
            if isinstance(value, datetime):
                return True
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} is not a valid date."