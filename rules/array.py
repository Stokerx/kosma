from . import Rule

class Array(Rule):
    def passes(self, attribute, value, parameters, validator):
        return isinstance(value, list)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be an array."