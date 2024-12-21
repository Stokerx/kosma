from . import Rule

class String(Rule):
    def passes(self, attribute, value, parameters, validator):
        return isinstance(value, str)

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be a string."