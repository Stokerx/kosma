from . import Rule

class InArray(Rule):
    def __init__(self, other_array):
        self.other_array = other_array

    def passes(self, attribute, value, parameters, validator):
        other_array_values = validator.data.get(self.other_array)
        if not isinstance(other_array_values, list):
            return False
        return value in other_array_values

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must exist in {self.other_array}."