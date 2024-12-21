from . import Rule

class Integer(Rule):
    def passes(self, attribute, value, parameters, validator):
        return str(value).lstrip('-').isdigit()

    def message(self, attribute, value, parameters, validator):
        return f"The {attribute} must be an integer."