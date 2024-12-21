import re
from . import Rule

class DigitsBetween(Rule):
    def __init__(self, min_length, max_length):
        self.min_length = min_length
        self.max_length = max_length

    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r'^\d{' + str(self.min_length) + r',' + str(self.max_length) + r'}$', str(value)))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be between {self.min_length} and {self.max_length} digits."