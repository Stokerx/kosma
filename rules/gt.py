from . import Rule
from kosma.utils import get_size

class Gt(Rule):
    def __init__(self, other):
        self.other = other

    def passes(self, attribute, value, parameters, validator):
        self.value = get_size(attribute, value, parameters, validator)
        self.other_value = get_size(self.other, validator.data.get(self.other), parameters, validator)
        return self.value > self.other_value

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be greater than {self.other}."