from . import Rule
from utils import get_size

class Min(Rule):
    def __init__(self, min_value):
        self.min_value = min_value

    def passes(self, attribute, value, parameters, validator):
        return get_size(attribute, value, parameters, validator) >= float(self.min_value)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be at least {self.min_value}."