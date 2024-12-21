import re
from . import Rule

class Regex(Rule):
    def __init__(self, pattern):
        self.pattern = pattern

    def passes(self, attribute, value, parameters, validator):
        return bool(re.search(self.pattern, str(value)))

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} format is invalid."