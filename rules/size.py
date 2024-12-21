from . import Rule
from utils import get_size

class Size(Rule):
    def __init__(self, size_value):
        self.size_value = size_value

    def passes(self, attribute, value, parameters, validator):
        return get_size(attribute, value, parameters, validator) == float(self.size_value)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be {self.size_value}."