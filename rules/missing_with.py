from . import Rule

class MissingWith(Rule):
    def __init__(self, *fields):
        self.fields = fields

    def passes(self, attribute, value, parameters, validator):
        if any(field in validator.data for field in self.fields):
            return attribute not in validator.data
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must be missing when any of {', '.join(self.fields)} are present."