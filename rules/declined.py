from . import Rule

class Declined(Rule):
    def passes(self, attribute, value, parameters, validator):
        return value in [False, 'false', 0, '0', 'no', 'off']

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be declined."