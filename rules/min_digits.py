import re
from . import Rule

class MinDigits(Rule):
    def __init__(self, min_length):
        self.min_length = min_length

    def passes(self, attribute, value, parameters, validator):
        if not str(value).isdigit():
            return False
        return len(str(value)) >= int(self.min_length)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must have at least {self.min_length} digits."

