from . import Rule

class MissingIf(Rule):
    def __init__(self, another_field, *values):
        self.another_field = another_field
        self.values = values

    def passes(self, attribute, value, parameters, validator):
        if validator.data.get(self.another_field) in self.values:
            return attribute not in validator.data
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must be missing when {self.another_field} is one of {', '.join(self.values)}."