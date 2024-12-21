from . import Rule

class NotIn(Rule):
    def __init__(self, *values):
        self.values = values

    def passes(self, attribute, value, parameters, validator):
        return str(value) not in self.values

    def message(self, attribute, value, parameters, validator):
        return f"The selected {attribute} is invalid."