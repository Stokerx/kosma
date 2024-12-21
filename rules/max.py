from . import Rule
from utils import get_size

class Max(Rule):
    def __init__(self, max_value):
        self.max_value = max_value

    def passes(self, attribute, value, parameters, validator):
        return get_size(attribute, value, parameters, validator) <= float(self.max_value)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} may not be greater than {self.max_value}."