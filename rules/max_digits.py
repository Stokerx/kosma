import re
from . import Rule

class MaxDigits(Rule):
    def __init__(self, max_length):
        self.max_length = max_length

    def passes(self, attribute, value, parameters, validator):
        if not str(value).isdigit():
            return False
        return len(str(value)) <= int(self.max_length)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must not have more than {self.max_length} digits."
