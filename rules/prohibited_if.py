from . import Rule

class ProhibitedIf(Rule):
    def __init__(self, other, value):
        self.other = other
        self.value = value

    def passes(self, attribute, value, parameters, validator):
        if validator.data.get(self.other) == self.value:
            return attribute not in validator.data
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field is prohibited when {self.other} is {self.value}."