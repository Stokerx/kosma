from . import Rule

class MissingWithAll(Rule):
    def __init__(self, *fields):
        self.fields = fields

    def passes(self, attribute, value, parameters, validator):
        if all(field in validator.data for field in self.fields):
            return attribute not in validator.data
        return True

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must be missing when all of {', '.join(self.fields)} are present."