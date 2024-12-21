from . import Rule

class Missing(Rule):
    def passes(self, attribute, value, parameters, validator):
        return attribute not in validator.data

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must be missing."