from . import Rule

class Boolean(Rule):
    def passes(self, attribute, value, parameters, validator):
        return value in [True, False, 0, 1, '0', '1']

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must be true or false."