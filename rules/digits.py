import re
from . import Rule

class Digits(Rule):
    def __init__(self, length):
        self.length = length

    def passes(self, attribute, value, parameters, validator):
        return bool(re.match(r'^\d{' + str(self.length) + r'}$', str(value)))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be {self.length} digits."