from . import Rule
from utils import get_size

class Between(Rule):
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def passes(self, attribute, value, parameters, validator):
        self.size = get_size(attribute, value, parameters, validator)
        return self.size >= float(self.min_val) and self.size <= float(self.max_val)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be between {self.min_val} and {self.max_val}."