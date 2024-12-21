from . import Rule

class Accepted(Rule):
    def passes(self, attribute, value, parameters, validator):
        return value in [True, 'true', 1, '1', 'yes', 'on']

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be accepted."