from . import Rule

class Present(Rule):
    def passes(self, attribute, value, parameters, validator):
        return attribute in validator.data

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must be present."