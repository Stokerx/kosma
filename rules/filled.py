from . import Rule

class Filled(Rule):
    def passes(self, attribute, value, parameters, validator):
        return value is not None and str(value).strip() != ''

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} field must have a value."