from . import Rule

class DeclinedIf(Rule):
    def __init__(self, other, value):
        self.other = other
        self.value = value

    def passes(self, attribute, value, parameters, validator):
        other_value = validator.data.get(self.other)
        if str(other_value).lower() == str(self.value).lower():
            return value in [False, 'false', 0, '0', 'no', 'off']
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be declined when {self.other} is {self.value}."