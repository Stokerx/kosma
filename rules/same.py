from . import Rule

class Same(Rule):
    def __init__(self, other_field):
        self.other_field = other_field

    def passes(self, attribute, value, parameters, validator):
        return value == validator.data.get(self.other_field)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} and {self.other_field} must match."