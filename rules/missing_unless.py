from . import Rule

class MissingUnless(Rule):
    def __init__(self, another_field, value):
        self.another_field = another_field
        self.value = value

    def passes(self, attribute, value, parameters, validator):
        if validator.data.get(self.another_field) != self.value:
            return attribute not in validator.data
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must be missing unless {self.another_field} is {self.value}."